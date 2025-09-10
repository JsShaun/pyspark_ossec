from pyspark.sql import functions as F 
from regular.linux_event_mapping import get_event_mapping  # 导入您的Linux事件映射表
from hpspark import NewSpark
from helper import KafkaProducer,KafkaConsumer

 
class OSSEC:
    def __init__(self):
        # 1. 初始化SparkSession
        self.spark = NewSpark(url="sc://localhost:15002",name="syslogProcessApp").get_spark()
        self.broadcasted_event_df = F.broadcast(self.spark.createDataFrame(get_event_mapping())) # 广播表到所有节点

    def new_df_msg(self, msglist:list):
        self.broadcasted_event_df.createOrReplaceTempView('tbevent')
        df = self.spark.createDataFrame(msglist).withColumn("id",F.monotonically_increasing_id())
        # 提取核心字段hostname(主机名)、program（程序）、日志记录（msg）
        syslog_pattern = r"""(\S+)\s+(\S+)\[\d+\]:\s*(.*)"""

        df.select(
            F.col("id"),
            F.col("value").alias("original_msg"),
            F.col('timestamp'),
            F.regexp_extract(F.col("value"), syslog_pattern, 1).alias("hostname"),
            F.regexp_extract(F.col("value"), syslog_pattern, 2).alias("program"),
            F.regexp_extract(F.col("value"), syslog_pattern, 3).alias("msg"),
        ).createOrReplaceTempView('tbmsg')

        df = self.spark.sql('''
        select *
        from tbmsg tb1
        left join tbevent tb2 on tb1.original_msg RLIKE tb2.regex
        ''')
        
        result_df = df.select(
            F.col("id"),
            F.col("original_msg"),
            F.col("tb1.hostname"),
            F.col("tb1.program"),
            F.col("event_cn"),
            F.col("event_type"),
            F.col("level"),
            F.col("level_cn"),
            F.col("log_category"),
            F.col("timestamp"),
        )
        # result_df.show()
        p1 = KafkaProducer(bootstrap_servers = '192.168.64.1:9092')
        for row in result_df.toLocalIterator():
            # print('发送row：',row)
            p1.send(topic='linux_rejieguo', partition=0, data=row.asDict())



if __name__ == "__main__":

    oss = OSSEC()
    # 创建并启动消费者
    consumer = KafkaConsumer(bootstrap_servers="localhost:9092", group_id="sample_consumer_group_v2")
    for msglist in  consumer.receive_batch(topic='Linux',partitions=[0]):
        oss.new_df_msg(msglist)

    # msg1 = "Sep 02 08:30:15 server01 sshd[1234]: Accepted password for jdoe from 192.168.1.100 port 54321 ssh2"
    # msg2 = "Sep 02 08:35:20 server01 sshd[5678]: Failed password for invalid user admin from 10.0.0.1 port 9876 ssh2"
    # msg3 = "Sep 02 10:05:22 server02 kernel[7890]: USB device not accepting address 5, error -71"
    # msg5 = "Sep 02 14:30:45 web01 firewalld[9012]: REJECT: IN=eth0 OUT= MAC=xx:xx:xx SRC=10.0.0.5 DST=192.168.1.10"
    # msg6 = "Sep 02 15:00:00 db01 nginx[2345]: 192.168.1.200 - - \"GET /index.html HTTP/1.1\" 200 1234"
    # msglist = []
    # msglist.append({'value':msg1,'id':1,'timestamp':1757065656})
    # msglist.append({'value':msg2,'id':2,'timestamp':1757065656})
    # msglist.append({'value':msg3,'id':3,'timestamp':1757065656})
    # # msglist.append({'value':msg4,'id':4})
    # msglist.append({'value':msg5,'id':5,'timestamp':1757065656})
    # msglist.append({'value':msg6,'id':6,'timestamp':1757065656})
    # oss.new_df_msg(msglist)
   





