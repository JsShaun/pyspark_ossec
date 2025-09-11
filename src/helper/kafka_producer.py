import json
import time
import os
from typing import Dict, List, Optional, Union
from confluent_kafka import Producer
from datetime import datetime


class KafkaProducer:
    """
    Kafka生产者封装类
    支持单条字典/列表数据输入，自动批量发送
    满足100条消息或1秒超时条件时自动发送
    日志自动写入文件，无需手动调用flush
    """
    
    def __init__(
        self, 
        bootstrap_servers: str,
        batch_size: int = 100,
        batch_timeout: int = 1,
        log_dir: str = "kafka_logs"
    ):
        """
        初始化Kafka生产者
        
        :param bootstrap_servers: Kafka broker地址
        :param batch_size: 批量发送的消息数量阈值
        :param batch_timeout: 批量发送的超时时间(秒)
        :param log_dir: 日志文件存储目录
        """
        # Kafka生产者配置
        self.config = {
            'bootstrap.servers': bootstrap_servers,
            'acks': 'all',
            'retries': 3,
            'linger.ms': 5,
            'batch.size': 16384
        }
        
        # 批量发送参数
        self.batch_size = batch_size
        self.batch_timeout = batch_timeout
        self.message_buffer = []
        self.last_send_time = time.time()
        self.current_topic = None
        self.current_partition = None
        
        # 初始化Kafka生产者
        self.producer = Producer(self.config)
        
        # 日志配置
        self.log_dir = log_dir
        self._init_log_dir()
        
        # 注册退出时的清理函数
        import atexit
        atexit.register(self._auto_flush_on_exit)

    def _init_log_dir(self) -> None:
        """初始化日志目录"""
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir, exist_ok=True)

    def _get_log_file_path(self) -> str:
        """获取当前日志文件路径（按日期命名）"""
        today = datetime.now().strftime("%Y-%m-%d")
        return os.path.join(self.log_dir, f"kafka_producer_{today}.log")

    def _write_log(self, level: str, message: str) -> None:
        """
        写入日志到文件
        
        :param level: 日志级别(INFO/ERROR/WARNING)
        :param message: 日志内容
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"[{timestamp}] [{level}] {message}\n"
        
        try:
            with open(self._get_log_file_path(), "a", encoding="utf-8") as f:
                f.write(log_line)
        except Exception as e:
            # 日志写入失败时不影响主流程，仅打印到控制台
            print(f"日志写入失败: {str(e)}, 日志内容: {log_line}")

    def _delivery_report(self, err, msg) -> None:
        """消息发送结果回调函数"""
        if err is not None:
            self._write_log("ERROR", f"消息发送失败: {err}")
        else:
            self._write_log("INFO", 
                          f"消息发送成功 - 主题: {msg.topic()}, "
                          f"分区: {msg.partition()}, 偏移量: {msg.offset()}")

    def _send_batch(self) -> None:
        """内部方法：发送缓冲区中的批量消息"""
        if not self.message_buffer:
            return
            
        try:
            # 发送缓冲区中的所有消息
            for msg in self.message_buffer:
                self.producer.produce(
                    topic=self.current_topic,
                    value=msg,
                    partition=self.current_partition,
                    on_delivery=self._delivery_report
                )
            
            # 处理回调
            self.producer.poll(0)
            
        except BufferError:
            self._write_log("WARNING", "消息缓冲区已满，等待处理...")
            self.producer.poll(1)
        except Exception as e:
            self._write_log("ERROR", f"发送消息时出错: {str(e)}")
        finally:
            # 刷新并检查剩余消息
            remaining = self.producer.flush()
            if remaining == 0:
                self._write_log("INFO", f"成功发送 {len(self.message_buffer)} 条消息")
            else:
                self._write_log("ERROR", f"仍有 {remaining} 条消息未发送，请检查Kafka状态")
            
            # 重置缓冲区和计时器
            self.message_buffer = []
            self.last_send_time = time.time()

    def send(self, topic: str, partition: Optional[int], data: Union[Dict, List[Dict]]) -> None:
        """
        发送消息（支持单条字典或列表数据）
        
        :param topic: 目标主题
        :param partition: 目标分区
        :param data: 单条消息(字典)或多条消息(字典列表)
        """
        # 统一转换为列表处理
        if isinstance(data, dict):
            data_list = [data]
        elif isinstance(data, list):
            # 过滤无效元素
            data_list = [item for item in data if isinstance(item, dict)]
            if len(data_list) < len(data):
                self._write_log("WARNING", 
                              f"过滤掉 {len(data) - len(data_list)} 个非字典类型的无效消息")
        else:
            self._write_log("ERROR", 
                          f"不支持的数据类型: {type(data)}，请使用字典或字典列表")
            return

        if not data_list:
            self._write_log("WARNING", "没有有效的消息需要处理")
            return

        # 主题/分区变化时先发送缓冲区消息
        if self.message_buffer:
            if topic != self.current_topic or partition != self.current_partition:
                self._write_log("INFO", "主题或分区变化，发送缓冲区中的消息")
                self._send_batch()
        
        # 更新当前主题和分区
        self.current_topic = topic
        self.current_partition = partition
        
        # 序列化消息并添加到缓冲区
        try:
            for item in data_list:
                msg = json.dumps(item).encode('utf-8')
                self.message_buffer.append(msg)
            
            self._write_log("INFO", 
                          f"已添加 {len(data_list)} 条消息到缓冲区，当前缓冲区大小: {len(self.message_buffer)}")
        except Exception as e:
            self._write_log("ERROR", f"消息序列化失败: {str(e)}")
            return
        
        # 检查发送条件
        current_time = time.time()
        if (len(self.message_buffer) >= self.batch_size) or \
           (current_time - self.last_send_time >= self.batch_timeout):
            self._write_log("INFO", 
                          f"满足发送条件 - 消息数: {len(self.message_buffer)}, "
                          f"时间差: {current_time - self.last_send_time:.2f}秒")
            self._send_batch()

    def _auto_flush_on_exit(self) -> None:
        """程序退出时自动发送剩余消息（无需手动调用）"""
        if self.message_buffer:
            self._write_log("INFO", f"程序退出，自动发送剩余的 {len(self.message_buffer)} 条消息")
            self._send_batch()

if __name__ == "__main__":

    p1 = KafkaProducer(bootstrap_servers = '192.168.64.1:9092')


    msg1 = "Sep 02 08:30:15 server01 sshd[1234]: Accepted password for jdoe from 192.168.1.100 port 54321 ssh2"
    msg2 = "Sep 02 08:35:20 server01 sshd[5678]: Failed password for invalid user admin from 10.0.0.1 port 9876 ssh2"
    msg3 = "Sep 02 10:05:22 server02 kernel[7890]: USB device not accepting address 5, error -71"
    msg5 = "Sep 02 14:30:45 web01 firewalld[9012]: REJECT: IN=eth0 OUT= MAC=xx:xx:xx SRC=10.0.0.5 DST=192.168.1.10"
    msg6 = "Sep 02 15:00:00 db01 nginx[2345]: 192.168.1.200 - - \"GET /index.html HTTP/1.1\" 200 1234"

    msglist = []
    msglist.append({'value':msg1,'id':1})
    msglist.append({'value':msg2,'id':2})
    msglist.append({'value':msg3,'id':3})
    msglist.append({'value':msg5,'id':5})
    msglist.append({'value':msg6,'id':6})
    # 要发送的消息
    
    # p1.send(topic='linux_original', partition=0, data=msglist)
    p1.send(topic='topic1111', partition=0, data=msglist)


