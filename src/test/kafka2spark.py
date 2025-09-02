from confluent_kafka import Consumer
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType, DateType, LongType
from helper.kafka_consumer import KafkaConsumer

            


# 配置参数
config = {
    "bootstrap_servers": "localhost:9092",
    "group_id": "sample_consumer_group_v2",
}

# 创建并启动消费者
consumer = KafkaConsumer(**config)

spark = SparkSession.builder \
    .remote("sc://localhost:15002") \
    .appName("CreateDataFrameWithPolars") \
    .getOrCreate()

schema = StructType([
    StructField("action", StringType(), nullable=True),
    StructField("id", IntegerType(), nullable=False),
    StructField("item", StringType(), nullable=True),
    StructField("status", StringType(), nullable=True),
    StructField("value", FloatType(), nullable=True),
    StructField("timestamp", LongType(), nullable=False)
])

for data in consumer.receive_batch(topics=['sample_topic2']):
    df_from_dict = spark.createDataFrame(data,schema)
    print("\n=== 从字典列表创建的 DataFrame ===")
    df_from_dict.show()
    df_from_dict.printSchema()
        

