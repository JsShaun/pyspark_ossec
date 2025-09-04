from pyspark.sql.functions import regexp_extract, col, broadcast
from regular.nginx_event_mapping import get_event_mapping  # 导入您的Linux事件映射表
from hpspark import NewSpark


class OSSEC:
    def __init__(self):
        # 1. 初始化SparkSession
        self.spark = NewSpark(url="sc://localhost:15002",name="pandasApp").get_spark()
        self.broadcasted_event_df = broadcast(self.spark.createDataFrame(get_event_mapping())) # 广播表到所有节点
        self.broadcasted_event_df.createOrReplaceTempView('tbevent')
     
 
    def new_df_msg(self, msglist:list):
        df = self.spark.createDataFrame(msglist)
        syslog_pattern = r"(\S+)\s+(\S+)\[\d+\]:\s*(\d+\.\d+\.\d+\.\d+)\s*(.*)"
        
        # 提取核心字段hostname(主机名)、program（程序）、日志记录（msg）
        df.select(
            col("id"),
            col("value").alias("original_msg"),
            regexp_extract(col("value"), syslog_pattern, 1).alias("hostname"),
            regexp_extract(col("value"), syslog_pattern, 2).alias("program"),
            regexp_extract(col("value"), syslog_pattern, 3).alias("client"),
            regexp_extract(col("value"), syslog_pattern, 4).alias("msg"),
        ).createOrReplaceTempView('tbmsg')


        self.spark.sql('''
        select *
        from tbmsg tb1
        left join tbevent tb2 on tb1.original_msg RLIKE tb2.event_regex
        ''').show()


if __name__ == "__main__":
    msg1 = """Sep 05 08:30:15 web01 nginx[28456]: 113.108.22.45 - - [05/Sep/2025:08:30:15 +0800] "POST /api/user/login HTTP/1.1" 200 128 "https://example.com/login" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/116.0.0.0"""
    msg2 = """Sep 05 08:30:20 web01 nginx[28456]: 113.108.22.45 - - [05/Sep/2025:08:30:20 +0800] "GET /static/css/main.css HTTP/1.1" 200 3562 "https://example.com/home" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/116.0.0.0"""
    msg3 = """Sep 06 10:15:30 web01 nginx[28456]: 198.51.100.78 - - [06/Sep/2025:10:15:30 +0800] "GET /search?query=手机' UNION SELECT username,password FROM users-- HTTP/1.1" 400 189 "-" "curl/7.68.0"""
    msg4 = """Sep 06 10:20:12 web01 nginx[28456]: 203.0.113.42 - - [06/Sep/2025:10:20:12 +0800] "POST /comment HTTP/1.1" 200 256 "https://example.com/article" "Mozilla/5.0" Request Body: content=<script>alert(document.cookie)</script>"""
    msg5 = """Sep 06 10:25:45 web01 nginx[28456]: 192.0.2.105 - - [06/Sep/2025:10:25:45 +0800] "GET /file?path=/var/log/nginx/access.log;cat /etc/passwd HTTP/1.1" 500 210 "-" "Wget/1.21"""
    msg6= """Sep 06 10:30:22 web01 nginx[28456]: 185.199.108.153 - - [06/Sep/2025:10:30:22 +0800] "GET /static/../../../../etc/shadow HTTP/1.1" 403 162 "-" "Mozilla/5.0"""
    msg7 = """Sep 07 09:20:18 web01 nginx[28456]: 192.0.2.110 - - [07/Sep/2025:09:20:18 +0800] "POST /login HTTP/1.1" 200 320 "https://example.com/login" "Chrome/116.0.0.0" Request Body: username=admin' AND (SELECT 1 FROM (SELECT COUNT(*),CONCAT((SELECT version()),FLOOR(RAND(0)*2))x FROM information_schema.tables GROUP BY x)a)-- &password=123"""



    msglist = []
    msglist.append({'value':msg1,'id':1})
    msglist.append({'value':msg2,'id':2})
    msglist.append({'value':msg3,'id':3})
    msglist.append({'value':msg4,'id':4})
    msglist.append({'value':msg5,'id':5})
    msglist.append({'value':msg6,'id':6})
    msglist.append({'value':msg7,'id':7})
   
    
    oss = OSSEC()
    oss.new_df_msg(msglist)
