
## 以下为调试笔记
### 使用脚本下载kafka读写jar包 —— 无法在worker发送kafka
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