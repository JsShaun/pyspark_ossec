from pyspark.sql import SparkSession
import json
import sys
from hpspark import NewSpark



# 初始化 Spark 会话
def init_spark():
    return NewSpark(url="sc://localhost:15002", name="syslogProcessApp").get_spark()

# Kafka 配置 - 仅返回配置字典，不在此处创建 Producer
def get_kafka_config():
    return {
        "bootstrap.servers": "192.168.64.1:9092",
        "acks": "1",
        "batch.size": 16384,
        "linger.ms": 5,
        "compression.type": "gzip",
        "error_cb": lambda err: print(f"Kafka 错误: {err}", file=sys.stderr)
    }

# 分区处理函数 - 完全隔离 Producer 的创建
def write_to_kafka(partition_iterator):

    pass
    # # 关键修复：在函数内部导入 Producer，避免在 Driver 端被序列化
    from confluent_kafka import Producer
    
    # # 在每个分区本地创建 Producer
    producer = Producer(get_kafka_config())

    
    try:
        for row in partition_iterator:
            # 转换数据为字典并序列化为 JSON 字节
            record = {
                "id": row.id,
                "value": row.value,
                "timestamp": row.timestamp
            }
            json_value = json.dumps(record, ensure_ascii=False).encode('utf-8')
            key = str(row.id).encode('utf-8')
            
            # 发送消息
            producer.produce(
                topic="target_topic",
                key=key,
                value=json_value
            )
            
        else:
            producer.poll(0)
            # 确保所有消息都被发送
            
        
    except Exception as e:
        print(f"处理分区时出错: {str(e)}", file=sys.stderr)
        raise
    finally:
        producer.flush()
        # 关闭生产者
        producer.close()
        


def main():
    spark = init_spark()
    
    # 示例数据
    data = [
        (1, "message 1", 1629260000),
        (2, "message 2", 1629260001),
        (3, "message 3", 1629260002)
    ]
    df = spark.createDataFrame(data, ["id", "value", "timestamp"])
    
    # 写入 Kafka
    df.foreachPartition(write_to_kafka)
    df.show()
    spark.stop()

if __name__ == "__main__":
    main()
    