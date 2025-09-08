from confluent_kafka import Producer
import json
import logging


# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class  KafkaProducer():

    def __init__(self,bootstrap_servers):
        config = {
            'bootstrap.servers': bootstrap_servers,
            'acks': 'all',  # 确保消息被所有ISR副本确认
            'retries': 3,   # 发送失败时重试次数
            'linger.ms': 5, # 批处理延迟，单位毫秒
            'batch.size': 16384  # 批处理大小，单位字节
        }
        self.producer = Producer(config)

    def delivery_report(self, err, msg):
        if err is not None:
            logger.error(f'消息发送失败: {err}')
        else:
            logger.info(f'消息发送成功 - 主题: {msg.topic()}, 分区: {msg.partition()}, 偏移量: {msg.offset()}')

    def send(self,topic,partition,messages):
        try:
            for data in messages:
                msg = json.dumps(data).encode('utf-8')
                self.producer.produce(
                    topic=topic,
                    value=msg,
                    partition=partition,
                    on_delivery=self.delivery_report
                )
            else:
                # 定期轮询以处理回调和发送队列
                self.producer.poll(0)

        except BufferError:
            logger.warning('消息缓冲区已满，等待处理...')
            self.producer.poll(1)  # 等待1秒
        except Exception as e:
            logger.error(f'发送消息时出错: {str(e)}')
        finally:
            logger.info("等待所有消息发送到Kafka集群...")
            remaining = self.producer.flush()  # 返回未发送的消息数
            if remaining == 0:
                logger.info("所有消息已成功发送")
            else:
                logger.error(f"仍有 {remaining} 条消息未发送，请检查Kafka状态")
            



if __name__ == "__main__":

    p1 = KafkaProducer(bootstrap_servers = 'localhost:9092')


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
    
    p1.send(topic='Linux', partition=0, messages=msglist)

