from confluent_kafka import Consumer
import json
import logging


# 配置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - [KafkaConsumer] - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class KafkaConsumer:
    def __init__(self, bootstrap_servers: str, group_id: str, auto_offset_reset: str = "earliest"):
        """初始化Kafka消费者助手"""
        self.consumer = Consumer(**{
            "bootstrap.servers": bootstrap_servers,
            "group.id": group_id,
            "auto.offset.reset": auto_offset_reset,
            "enable.auto.commit": False,  # 禁用自动提交，手动控制
            "heartbeat.interval.ms": 3000,
            "session.timeout.ms": 30000
        })
        
    def receive_batch(self, topics:list, batch_size=10, max_wait=5):
        import time
        self.consumer.subscribe(topics)
        logger.info(f"消费者已启动，订阅主题: {topics}")
        batch = []
        start_time = time.time()
        while 1:
            elapsed = (time.time() - start_time)
            remaining = max(0, max_wait - elapsed)
            if (remaining <= 0 or len(batch) > batch_size) and len(batch) > 0:
                yield batch
                self.consumer.commit()
                logger.info(f"已提交 {len(batch)} 条消息的偏移量")
                batch = []
                start_time = time.time()

            msg = self.consumer.poll(timeout=remaining)
            if msg is None:
                pass
            elif msg.error():
                logger.error(f"错误码：{msg.error().code()}:{msg.error().str()}")
            else:
                logger.info(f"主题: {msg.topic()} - 分区: {msg.partition()} - 偏移量: {msg.offset()}")
                _, timestamp_ms = msg.timestamp()
                data = json.loads(msg.value().decode('utf-8'))
                data['timestamp'] = timestamp_ms
                batch.append(data)


if __name__ == "__main__":
    # 配置参数
    config = {
        "bootstrap_servers": "localhost:9092",
        "group_id": "sample_consumer_group_v2",
    }
    # 创建并启动消费者
    consumer = KafkaConsumer(**config)
    for data in  consumer.receive_batch(topics=['Linux']):
        print("data: ",data)

