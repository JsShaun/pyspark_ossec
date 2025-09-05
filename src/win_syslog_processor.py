from pyspark.sql.functions import regexp_extract, col, broadcast
from regular.windows_event_mapping import get_event_mapping
from hpspark import NewSpark


class OSSEC:
    def __init__(self):
        # 初始化SparkSession
        self.spark = NewSpark(url="sc://localhost:15002",name="pandasApp").get_spark()
        self.broadcasted_event_df = broadcast(self.spark.createDataFrame(get_event_mapping())) # 广播表到所有节点
         
        


    def new_df_msg(self,msglist:list):
        self.broadcasted_event_df.createOrReplaceTempView('tbevent') 
        df = self.spark.createDataFrame(msglist)
        # 定义基本Windows事件日志的正则表达式模式
        base_pattern = r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (\S+) MSWinEventLog: (\d+), ([^,]+), (\d+), (\d{2}:\d{2}:\d{2} \d{2}/\d{2}/\d{4}), (\d+), ([^,]+), ([^,]*), ([^,]*), ([^,]+), '
        # 提取基本字段
        df.select(
            col('id'),
            col("value").alias("original_msg"),
            regexp_extract(col("value"), base_pattern, 1).alias("receive_time"),
            regexp_extract(col("value"), base_pattern, 2).alias("hostname"),
            regexp_extract(col("value"), base_pattern, 3).alias("event_type_code"),
            regexp_extract(col("value"), base_pattern, 4).alias("log_type"),
            regexp_extract(col("value"), base_pattern, 5).alias("event_record_number"),
            regexp_extract(col("value"), base_pattern, 6).alias("event_time"),
            regexp_extract(col("value"), base_pattern, 7).alias("event_id"),
            regexp_extract(col("value"), base_pattern, 8).alias("event_source"),
            regexp_extract(col("value"), base_pattern, 9).alias("event_category"),
            regexp_extract(col("value"), base_pattern, 10).alias("event_level"),
            regexp_extract(col("value"), base_pattern, 11).alias("computer_name"),
        ).createOrReplaceTempView('tbmsg')


    def df_parsed_logs(self):
        parsed_logs = self.spark.sql("""
        select *
        from tbmsg tb1
        left join tbevent tb2 on tb1.event_id = tb2.event_id
        """).select(
            col('id'),
            col('hostname'),
            col('tb1.event_id'),
            col('event_cn'),
            col('event_source'),
            col('event_type'),
            col('level'),
            col('level_cn'),
            col('event_time'),
            col('log_category'),
        )
        parsed_logs.show()




if __name__ == "__main__":

    msg1 = r"""2025-09-02 08:30:15 WIN-SERVER MSWinEventLog: 0, Security, 15678, 08:30:12 09/02/2025, 4624, Microsoft-Windows-Security-Auditing, , , WIN-SERVER, 
An account was successfully logged on.
Subject:
    Security ID:        S-1-0-0
    Account Name:       -
    Account Domain:     -
    Logon ID:       0x0
Logon Type:         3
New Logon:
    Security ID:        S-1-5-21-3623811015-3361044348-30300820-1013
    Account Name:       jdoe
    Account Domain:     CORP
    Logon ID:       0x1A2B3C4D
    Logon GUID:     {00000000-0000-0000-0000-000000000000}
Process Information:
    Process ID:     0x0
    Process Name:       -
Network Information:
    Workstation Name:   -
    Source Network Address: 192.168.1.105
    Source Port:        54321
Detailed Authentication Information:
    Logon Process:      NtLmSsp 
    Authentication Package: NTLM
    Transited Services: -
    Package Name (NTLM only): NTLM V2
    Key Length:     128
    """

    msg2 = r"""2025-09-02 09:15:42 DESKTOP-PC MSWinEventLog: 0, Security, 15679, 09:15:40 09/02/2025, 4688, Microsoft-Windows-Security-Auditing, , , DESKTOP-PC, 
A new process has been created.
Subject:
    Security ID:        S-1-5-21-3623811015-3361044348-30300820-1013
    Account Name:       jdoe
    Account Domain:     CORP
    Logon ID:       0x1A2B3C4D
Process Information:
    New Process ID:     0x1234
    New Process Name:   C:\Windows\System32\notepad.exe
    Token Elevation Type:   %%1936
    Creator Process ID: 0x5678
    Creator Process Name:   C:\Windows\explorer.exe
    Process Command Line:   "C:\Windows\notepad.exe" "C:\Users\jdoe\Documents\notes.txt"cdcd
    """

    msglist = []
    msglist.append({'value':msg1,'id':1})
    msglist.append({'value':msg2,'id':2})

    o = OSSEC()
    o.new_df_msg(msglist)
    o.df_parsed_logs()
    