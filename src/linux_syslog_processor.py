from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_extract, col, when, lit, concat
from pyspark.sql.types import StringType
from regular.linux_event_mapping import get_event_mapping  # 导入您的Linux事件映射表
from hpspark import NewSpark


class OSSEC:
    def __init__(self):
        # 1. 初始化SparkSession
        self.spark = NewSpark(url="sc://localhost:15002",name="pandasApp").get_spark()
        self.event_mapping = self.spark.createDataFrame(get_event_mapping()).createOrReplaceTempView('tbevent')
        
  
        
        # 3. 定义事件匹配规则（与get_event_mapping()的event_id对应）
        self.event_rules = [
            # (进程名正则, 日志内容关键词正则, 目标event_id)
            (r"sshd", r"Accepted password for", "sshd-success"),
            (r"sshd", r"Failed password for", "sshd-failure"),
            (r"sudo", r"session opened for user root", "sudo-success"),
            (r"sudo", r"authentication failure", "sudo-failure"),
            (r"kernel", r"USB device not accepting address", "kernel-usb-error"),
            (r"kernel", r"Disk I/O error|bad sector", "kernel-disk-warning"),
            (r"kernel", r"network interface .* up", "kernel-network-up"),
            (r"CRON", r"CMD \(cd / && run-parts --report /etc/cron\.", "cron-exec-success"),
            (r"CRON", r"ERROR|failed to execute", "cron-exec-failure"),
            (r"systemd", r"Service started|Started .* service", "systemd-start"),
            (r"systemd", r"Service crashed|Failed with result", "systemd-crash"),
            (r"firewalld", r"REJECT|blocked", "firewalld-block"),
            (r"firewalld", r"ACCEPT|allowed", "firewalld-allow"),
            (r"app-server", r"Application started|Started successfully", "app-log-local0")
        ]

    def new_df_msg(self, msglist:list):
        df = self.spark.createDataFrame(msglist)
        # 2. 关键正则表达式：精准匹配主机名（位于时间和“进程名[PID]”之间）
        # 日志格式拆解：<优先级> 时间 主机名 进程名[PID]: 日志内容
        # 正则分组说明：
        # 1: 优先级（不提取）, 2: 时间（不提取）, 3: 主机名（核心：位于时间和进程名[PID]之间）
        # 4: 进程名（用于匹配event_id）, 5: 日志内容（用于匹配event_id）
        syslog_pattern = r"""
        ^<(\d+)>                # 优先级
            \s+([A-Za-z]{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})  # 时间
            \s+(\S+)                # 主机名
            \s+([^\:]+)             # 完整程序名（含PID，到冒号前结束）
            :.*                     # 剩余内容（不提取）
        """
        
        # 3. 提取核心字段（主机名、进程名、日志内容）
        parsed_df = df.select(
            col("id"),
            col("value"),
            regexp_extract(col("value"), syslog_pattern, 1).alias("value1"),
            regexp_extract(col("value"), syslog_pattern, 2).alias("value2"),
            regexp_extract(col("value"), syslog_pattern, 3).alias("value3"),
            regexp_extract(col("value"), syslog_pattern, 4).alias("value4"),
        )
        
        
        parsed_df.show()


if __name__ == "__main__":
    msg1 = "<13>Sep 02 08:30:15 server01 sshd[1234]: Accepted password for jdoe from 192.168.1.100 port 54321 ssh2"
    msg2 = "<11>Sep 02 08:35:20 server01 sshd[5678]: Failed password for invalid user admin from 10.0.0.1 port 9876 ssh2"
    msg3 = "<30>Sep 02 10:05:22 server02 kernel[7890]: USB device not accepting address 5, error -71"
    msg4 = "<142>Sep 02 12:00:00 server03 CRON[3456]: (root) CMD (cd / && run-parts --report /etc/cron.hourly)"
    msg5 = "<180>Sep 02 14:30:45 web01 firewalld[9012]: REJECT: IN=eth0 OUT= MAC=xx:xx:xx SRC=10.0.0.5 DST=192.168.1.10"
    msg6 = "<190>Sep 02 15:00:00 db01 nginx[2345]: 192.168.1.200 - - \"GET /index.html HTTP/1.1\" 200 1234"

    msglist = []
    msglist.append({'value':msg1,'id':1})
    msglist.append({'value':msg2,'id':2})
    msglist.append({'value':msg3,'id':3})
    msglist.append({'value':msg4,'id':4})
    msglist.append({'value':msg5,'id':5})
    msglist.append({'value':msg6,'id':6})
   
    
    oss = OSSEC()
    oss.new_df_msg(msglist)
