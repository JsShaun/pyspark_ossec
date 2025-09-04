from confluent_kafka import Consumer
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, LongType
from helper.kafka_consumer import KafkaConsumer

            


# 配置参数
config = {
    "bootstrap_servers": "localhost:9092",
    "group_id": "group_v1",
}

# 创建并启动消费者
consumer = KafkaConsumer(**config)

spark = SparkSession.builder \
    .remote("sc://localhost:15002") \
    .appName("AppLinux") \
    .getOrCreate()

schema = StructType([
    StructField("id", IntegerType(), nullable=False),
    StructField("value", StringType(), nullable=True),
    StructField("timestamp", LongType(), nullable=False)
])

for data in consumer.receive_batch(topics=['Linux']):
    df_from_dict = spark.createDataFrame(data,schema)
    df_from_dict.show()
    # df_from_dict.printSchema()
        

