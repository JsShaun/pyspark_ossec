from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType
# from .msg import message_udf # 示例pandas_udf使用
# from .msgevent import envent_udf




class NewSpark:

    def __init__(self,url,name):
        "sc://localhost:15002"
        self.spark = SparkSession.builder.remote(url).appName(name).getOrCreate()


        
        
    def get_spark(self):
        "注册自定义udf"
        # self.spark.udf.register("message_udf",message_udf)
        # self.spark.udf.register("envent_udf",envent_udf)
        return self.spark
        

    def result_schema(self):
        return StructType([
            StructField("print", StringType()),
        ])


        



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
            