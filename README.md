# pyspark_ossec


### python虚拟环境
- python3.10 -m venv .env
- source .env/bin/activate


# PySpark应用
## 先卸载所有相关包以避免残留
- pip3 uninstall -y protobuf grpcio grpcio-status googleapis-common-protos

## 安装兼容组合（重点确保 grpcio-status ≥1.48.1）
- pip3 install protobuf==6.32
- pip3 install grpcio==1.74
- pip3 install grpcio-status==1.74
- pip3 install googleapis-common-protos

## 安装pyspark库
- pip3 install pyspark==3.5.6
- pip3 install pandas
- pip3 install pyarrow


### 底层基于C语言实现，高效率
- pip3 install confluent-kafka



### 使用脚本下载kafka读写jar包
- ./bin/spark-shell --packages org.apache.spark:spark-sql-kafka-0-10_2.13:4.0.0 --repositories https://maven.aliyun.com/repository/public --conf spark.driver.host=localhost
- ./sbin/start-connect-server.sh --packages org.apache.spark:spark-sql-kafka-0-10_2.13:4.0.0

```py
    kafka_df = result_df.select(
        F.col("id").cast("string").alias("key"),   # 可选：将某个字段（如 id）转换为字符串作为 key（无 key 可删除这一行）
        F.to_json(F.struct("*")).alias("value")  # 必选：将所有字段打包为 JSON 字符串作为 value（或按需选择特定字段） struct("*") 表示所有字段，可替换为 struct("字段1", "字段2")
    )
    kafka_df.write \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "192.168.64.1:9092") \
    .option("topic", "topic1111") \
    .option("kafka.compression.type", "snappy") \
    .option("kafka.acks", "all") \
    .option("kafka.retries", "3") \
    .mode("append") \
    .save()
```