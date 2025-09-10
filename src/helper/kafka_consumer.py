from confluent_kafka import Consumer, TopicPartition
import json
import time
import os
from datetime import datetime
from typing import List, Union


class KafkaConsumer:
    def __init__(self, bootstrap_servers: str, group_id: str, log_dir: str = "kafka_logs"):
        # 1. 消费者基础配置
        self.consumer = Consumer({
            "bootstrap.servers": bootstrap_servers,
            "group.id": group_id,
            "auto.offset.reset": "earliest",  # 无偏移量时从最早开始
            "enable.auto.commit": False       # 手动提交偏移量
        })
        self.assigned_partitions = None  # 记录已分配的分区

        # 2. 日志基础配置（简化版）
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)  # 自动创建日志目录

    def _write_log(self, level: str, msg: str) -> None:
        """简化日志写入：按日期分文件，包含时间戳和级别"""
        log_file = os.path.join(self.log_dir, f"kafka_consumer_{datetime.now().strftime('%Y-%m-%d')}.log")
        log_line = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [{level}] {msg}\n"
        
        try:
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(log_line)
        except Exception as e:
            print(f"日志写入失败: {e} | 内容: {log_line.strip()}")

    def receive_batch(self, topic: str, partitions: Union[int, List[int]], batch_size: int = 10, max_wait: int = 5):
        """简化版批量消费：指定分区，满足条件返回批次"""
        # 1. 处理分区参数（统一转为列表）
        partition_list = [partitions] if isinstance(partitions, int) else partitions
        if any(p < 0 for p in partition_list):
            self._write_log("ERROR", "分区号不能为负数")
            return

        # 2. 分配指定分区
        self.assigned_partitions = [TopicPartition(topic, p) for p in partition_list]
        self.consumer.assign(self.assigned_partitions)
        self._write_log("INFO", f"已分配分区：主题[{topic}]，分区{partition_list}")

        batch = []
        start_time = time.time()

        try:
            while True:
                elapsed = time.time() - start_time
                remaining_wait = max(0, max_wait - elapsed)

                # 3. 满足条件则返回批次并提交偏移量
                if (len(batch) >= batch_size or remaining_wait <= 0) and batch:
                    yield batch
                    # 手动提交偏移量（提交到下一条待消费位置）
                    commit_offsets = [
                        TopicPartition(tp.topic, tp.partition, self.consumer.position([tp])[0].offset + 1)
                        for tp in self.assigned_partitions
                    ]
                    self.consumer.commit(offsets=commit_offsets)
                    self._write_log("INFO", f"提交{len(batch)}条消息偏移量")
                    batch = []
                    start_time = time.time()

                # 4. 拉取并解析消息
                msg = self.consumer.poll(timeout=remaining_wait)
                if msg is None:
                    continue
                if msg.error():
                    self._write_log("ERROR", f"消费错误: {msg.error()}")
                    continue

                try:
                    _, timestamp_ms = msg.timestamp()
                    data = json.loads(msg.value().decode('utf-8'))
                    data["partition"] = msg.partition()  # 补充分区信息
                    data['timestamp'] = timestamp_ms
                    batch.append(data)
                    self._write_log("DEBUG", f"收到消息：分区{msg.partition()}，偏移量{msg.offset()}")
                except json.JSONDecodeError:
                    self._write_log("ERROR", f"消息解析失败: {msg.value()}")

        except KeyboardInterrupt:
            self._write_log("INFO", "用户中断消费")
        finally:
            # 关闭前处理剩余消息
            if batch:
                yield batch
                self._write_log("INFO", f"消费中断，返回剩余{len(batch)}条消息")
            self.consumer.close()
            self._write_log("INFO", "消费者已关闭")


if __name__ == "__main__":
    # 配置参数
    config = {
        "bootstrap_servers": "192.168.64.1:9092",
        "group_id": "sample_consumer_group_v2",
    }
    # 创建并启动消费者
    consumer = KafkaConsumer(**config)
    for data in  consumer.receive_batch(topic='linux_original',partitions=[0]):
        print("data: ",data)

