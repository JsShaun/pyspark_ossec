
import warnings
warnings.filterwarnings('ignore')
import numpy as np
from sys import getsizeof
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import regexp_replace,regexp_extract,col,collect_list,when,udf
from pyspark.sql.types import StructType, StructField, StringType, ArrayType, BooleanType, IntegerType, MapType
import pandas as pd
import re
from regular.decoder import get_decoder_dataframe  # 返回pandas DataFrame
from regular.rules import get_rules_dataframe      # 返回pandas DataFrame
# from regular.rules_cn import RulesCN
from spark_herple import NewSpark



class OSSEC:
    def __init__(self):
        # 初始化SparkSession
        self.spark = NewSpark(url="sc://localhost:15002",name="pandasApp").get_spark()
        # df_decoder = get_decoder_dataframe()
        # self.spark.createDataFrame(df_decoder).createOrReplaceTempView('dfIsDecoder')
        # df_rules = get_rules_dataframe()
        # self.spark.createDataFrame(df_rules).createOrReplaceTempView('dfIsRules')


    def new_df_msg(self,msglist:list):
        df = self.spark.createDataFrame(msglist).createOrReplaceTempView('tbmsg')
        df = self.spark.sql("""
        select message_udf(msg) as processed
        from tbmsg
        """)

        df = df.select(
            col("processed").getField("original_msg").alias("original_msg"),
            col("processed").getField("full_event").alias("full_event"),
            col("processed").getField("processed_msg").alias("processed_msg"),
            col("processed").getField("hostname").alias("hostname"),
            col("processed").getField("program_name").alias("program_name"),
 
        )
        df.show()




if __name__ == "__main__":

    # ossec stable 版本查看：https://github.com/ossec/ossec-hids/tree/stable
    msg1 = """Jun 25 14:04:30 10.0.0.1 dropbear[30746]: Failed listening on '7001': Error listening: Address already in use""" 
    # # 正则参数问题，与下面的1002问题一样
    
    msg2 = """May  8 08:26:55 mail postfix/postscreen[22055]: NOQUEUE: reject: RCPT from [157.122.148.242]:47407: 550 5.7.1 Service unavailable; client [157.122.148.242] blocked using bl.spamcop.net; from=<kos@mafia.network>, to=<z13699753428@vip.163.com>, proto=ESMTP, helo=<XL-20160217QQJV>""" 
    
    # 按正则规则是正确的，可能与ossec规则有点不一样
    # 3302是正确的，因为id正则确实是符合的，而3306是不符的，ossec stable版本是符合正则的匹配的
    
    # msg = """2014-05-20T09:01:07.283219-04:00 arrakis unbound: [9405:0] notice: sendto failed: Can't assign requested address""" # 稳定版 rule_id=500100~ 不存在 1002结果也是不正确的，1002是普遍存在的
    
    # msg = """[Fri Dec 13 06:59:54 2013] [error] [client 12.34.65.78] PHP Notice:"""

    msglist = []
    msglist.append({'msg':msg1,'id':1})
    msglist.append({'msg':msg2,'id':2})

    o = OSSEC()
    o.new_df_msg(msglist)
  
   