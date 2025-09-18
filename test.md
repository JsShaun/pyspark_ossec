


## 以下为kafka应用调试
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



## mapInArrow polars应用开发
- pip3 install pyarrow polars
```py
def polars_func(iterator):
    '''使用polars数据处理'''
    import polars as pl
    for batch in iterator:
        df = pl.from_arrow(batch)
        # 在这里写polars处理逻辑
        arrow_table = df.to_arrow()
        for sub_batch in arrow_table.to_batches():
            yield sub_batch
df = result_df.mapInArrow(polars_func,df.schema)
```