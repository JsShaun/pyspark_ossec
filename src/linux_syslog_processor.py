from pyspark.sql.functions import regexp_extract, col, broadcast
from regular.linux_event_mapping import get_event_mapping  # 导入您的Linux事件映射表
from hpspark import NewSpark


class OSSEC:
    def __init__(self):
        # 1. 初始化SparkSession
        self.spark = NewSpark(url="sc://localhost:15002",name="pandasApp").get_spark()
        self.broadcasted_event_df = broadcast(self.spark.createDataFrame(get_event_mapping())) # 广播表到所有节点
        self.broadcasted_event_df.createOrReplaceTempView('tbevent')
     
 
    def new_df_msg(self, msglist:list):
        df = self.spark.createDataFrame(msglist)
        syslog_pattern = r"""(\S+)\s+(\S+)\[\d+\]:\s*(.*)"""
        
        # 提取核心字段hostname(主机名)、program（程序）、日志记录（msg）
        df.select(
            col("id"),
            col("value").alias("original_msg"),
            regexp_extract(col("value"), syslog_pattern, 1).alias("hostname"),
            regexp_extract(col("value"), syslog_pattern, 2).alias("program"),
            regexp_extract(col("value"), syslog_pattern, 3).alias("msg"),
        ).createOrReplaceTempView('tbmsg')


        self.spark.sql('''
        select *
        from tbmsg tb1
        left join tbevent tb2 on tb1.original_msg RLIKE tb2.regex
        ''').show()


if __name__ == "__main__":
    msg1 = "Sep 02 08:30:15 server01 sshd[1234]: Accepted password for jdoe from 192.168.1.100 port 54321 ssh2"
    msg2 = "Sep 02 08:35:20 server01 sshd[5678]: Failed password for invalid user admin from 10.0.0.1 port 9876 ssh2"
    msg3 = "Sep 02 10:05:22 server02 kernel[7890]: USB device not accepting address 5, error -71"
    msg5 = "Sep 02 14:30:45 web01 firewalld[9012]: REJECT: IN=eth0 OUT= MAC=xx:xx:xx SRC=10.0.0.5 DST=192.168.1.10"
    msg6 = "Sep 02 15:00:00 db01 nginx[2345]: 192.168.1.200 - - \"GET /index.html HTTP/1.1\" 200 1234"

    msglist = []
    msglist.append({'value':msg1,'id':1})
    msglist.append({'value':msg2,'id':2})
    msglist.append({'value':msg3,'id':3})
    # msglist.append({'value':msg4,'id':4})
    msglist.append({'value':msg5,'id':5})
    msglist.append({'value':msg6,'id':6})
   
    
    oss = OSSEC()
    oss.new_df_msg(msglist)
