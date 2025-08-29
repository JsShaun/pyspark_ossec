
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




spark = SparkSession.builder \
.remote("sc://localhost:15002") \
.appName("CreateDataFrameWithPolars") \
.getOrCreate()




# 定义返回类型结构（包含OK和msg两个字段）
result_schema = StructType([
    StructField("OK", BooleanType(), nullable=False),
    StructField("msg", StringType(), nullable=True)
])
def _program_name_pcre2_udf(program_name_pcre2, parent, program_name_flag, processed_msg, program_name):
    """
    PySpark UDF实现，对应原pandas的_program_name_pcre2方法
    参数:
        program_name_pcre2: 正则表达式字符串列表
        parent: parent字段值
        program_name_flag: 程序名标志(True/False)
        log: 日志内容
        program_name: 程序名
    """
    # 预编译所有正则表达式（带忽略大小写）
    patterns = [re.compile(pattern, re.IGNORECASE) for pattern in program_name_pcre2]
    if parent == "":
        # 遍历正则表达式进行匹配
        for pattern in patterns:
            # 尝试匹配program_name
            if pattern.search(program_name):
                # 匹配成功：清理日志前缀
                cleaned_log = re.sub(r"^(\S+): ", "", processed_msg)
                return (True, cleaned_log)
            else:
                # 第一个不匹配就返回False（原逻辑for循环中一旦不匹配就返回）
                return (False, "")
        
        # 循环正常结束（无匹配且列表非空）：根据flag处理
        if program_name_flag:
            cleaned_log = re.sub(r"^(\S+): ", "", processed_msg)
            return (True, cleaned_log)
        else:
            return (True, processed_msg)
    else:
        # parent不为空时返回False
        return (False, "")
# 注册UDF
program_name_pcre2_spark_udf = udf(_program_name_pcre2_udf, result_schema)


prematch_result_schema = StructType([
    StructField("OK", BooleanType(), nullable=False),  # 是否符合prematch规则
    StructField("span_start", IntegerType(), nullable=True),  # span起始位置
    StructField("span_end", IntegerType(), nullable=True)     # span结束位置
])
def _prematch_pcre2_udf(msg,offset_in_prematch_pcre2,parent,prematch_pcre2,decoder_name):
        '''第二步:prematch正则判定以及剔除对于字符
        根据prematch_pcre2规则,判断是否符合要求,如果符合则返回True且剔除对于的字符
        '''
        span = (0,0)
        if "after_parent" in offset_in_prematch_pcre2:
           
            if decoder_name == parent:
                pass
                # span = prematch_pcre2_span
                # for value in prematch_pcre2_span:
                #     msg = msg[prematch_pcre2_span[-1]:]
                    # span = value

        for pattern in prematch_pcre2:
            mobj = re.compile(pattern, re.IGNORECASE).search(msg)
            if mobj is not None:
                if mobj.group() == "":
                    pass
                else:
                    span = (0,span[1] + mobj.span()[1])
                    return True,*span
            else:
                return False,0, 0
        return True,None,None
prematch_pcre2_spark_udf = udf(_prematch_pcre2_udf, prematch_result_schema)

pcre2_result_schema = StructType([
    StructField("OK", BooleanType(), nullable=False),
    StructField("shijian", StringType(), nullable=False),
])
def _pcre2_udf(msg,offset_in_pcre2,decoder_name,parent,span_start,span_end,pcre2,order):
    '''第三步:pcre2正则获取对应的字段值
    完成或第一步且第二步之后.我们得到的log进行pcre2正则判定,并且可以抽取得到对应的order字段值
    '''
    if "after_parent" in offset_in_pcre2:
        if decoder_name == parent:
            msg = msg[span_end:]
                                    
    if "after_prematch" in offset_in_pcre2:
        msg = msg[span_start:]

    if "after_regex" in offset_in_pcre2:
        if decoder_name == decoder_name:
            for _ in offset_in_pcre2:
                for pattern in pcre2:
                    msg = re.compile(pattern, re.IGNORECASE).sub("",msg)      
    
    for pattern in pcre2:
        list1 = re.compile(pattern, re.IGNORECASE).findall(msg)
        flat_list = [item for sublist in list1 for item in (sublist if isinstance(sublist, tuple) else [sublist])]
        list2 = [x for x in flat_list if x != ""]

        # list1 = np.array(re.compile(pattern, re.IGNORECASE).findall(msg)).flatten()
        # list2 = np.delete(list1, np.where(list1==""))
        if len(list2) > 0:
            
            return True,str(dict(zip(order,list2)))
    else:
        return False,str({})
pcre2_spark_udf = udf(_pcre2_udf,pcre2_result_schema)


class OSSEC:
    def __init__(self,msglist:list):
        # 初始化SparkSession
  
        df_decoder = get_decoder_dataframe()
        spark.createDataFrame(df_decoder).createOrReplaceTempView('dfIsDecoder')
        df_rules = get_rules_dataframe()
        # spark.createDataFrame(df_rules).createOrReplaceTempView('dfIsRules')



        df = spark.createDataFrame(msglist)
                
        # 1. 替换多个空格为单个空格
        df = df.withColumn("full_event", regexp_replace(col("msg"), r"\s+", " ")) \
            .withColumn("processed_msg", col("full_event"))

        # 2. 移除不同格式的日期时间
        # 格式1: [Mon. Jan. 1 00:00:00 2023] 
        date_pattern1 = r"^\[(Mond?a?y?|Tues?d?a?y?|Wedn?e?s?d?a?y?|Thur?s?d?a?y?|Frid?a?y?|Satu?r?d?a?y?|Sund?a?y?)\.? (Janu?a?r?y?|Febr?u?a?r?y?|Marc?h?|Apri?l?|May|June?|July?|Augu?s?t?|Sept?e?m?b?e?r?|Octo?b?e?r?|Nove?m?b?e?r?|Dece?m?b?e?r?)\.? {1,2}\d{1,2} {1,2}\d{1,2}:\d{1,2}:\d{1,2} \d{4}\] ?"

        # 格式2: Jan 1 00:00:00 
        date_pattern2 = r"^(Janu?a?r?y?|Febr?u?a?r?y?|Marc?h?|Apri?l?|May|June?|July?|Augu?s?t?|Sept?e?m?b?e?r?|Octo?b?e?r?|Nove?m?b?e?r?|Dece?m?b?e?r?)\.? {1,2}(\d{1,2}) {1,2}(\d{1,2}:\d{1,2}:\d{1,2}) "

        # 格式3: 2023-1-1 00:00:00 或 2023-01-01T00:00:00+08:00
        date_pattern3 = r"^\d{4}-\d{1,2}-\d{1,2}(T| )(\d{1,2}:\d{1,2}:\d{2})(\S)+ "

        df = df.withColumn("processed_msg", regexp_replace(col("processed_msg"), date_pattern1, "")) \
            .withColumn("processed_msg", regexp_replace(col("processed_msg"), date_pattern2, "")) \
            .withColumn("processed_msg", regexp_replace(col("processed_msg"), date_pattern3, ""))

        # 3. 提取hostname
        hostname_pattern = r"^([^\f\n\r\t\v:]+) "
        df = df.withColumn("hostname", regexp_extract(col("processed_msg"), hostname_pattern, 1))

        # 4. 处理程序名并格式化
        # 提取程序部分
        program_pattern1 = r"^([^\f\n\r\t\v:]+ )?([^\f\n\r\t\v:]+\[\S+\]:? )"
        program_pattern2 = r"^([^\f\n\r\t\v:]+ )?([^\[\]\f\n\r\t\v]+: )"

        # 先尝试第一个程序模式
        df = df.withColumn("program_match", regexp_extract(col("processed_msg"), program_pattern1, 0)) \
            .withColumn("program_part", regexp_extract(col("processed_msg"), program_pattern1, 2))

        # 如果第一个模式没有匹配，尝试第二个模式
        df = df.withColumn("program_match", when(col("program_match") == "", regexp_extract(col("processed_msg"), program_pattern2, 0)).otherwise(col("program_match"))) \
            .withColumn("program_part",when(col("program_part") == "",regexp_extract(col("processed_msg"), program_pattern2, 2)).otherwise(col("program_part")))

        # 格式化程序部分
        df = df.withColumn("formatted_program", regexp_replace(col("program_part"), r"(\[\S+\])?:? ", ": ")) \
            .withColumn("processed_msg", regexp_replace(col("processed_msg"), col("program_match"), col("formatted_program")))

        # 提取程序名
        df = df.withColumn("program_name", regexp_extract(col("formatted_program"), r"^(\S+): ?", 1))

        # 5. 替换大括号为引号
        df = df.withColumn("processed_msg", regexp_replace(col("processed_msg"), r"\{", '"')) \
            .withColumn("processed_msg", regexp_replace(col("processed_msg"), r"\}", '"'))

        # 选择最终需要的列
        df.select(
            col("id"),
            col("msg").alias("original_msg"),
            col("full_event"),
            col("processed_msg"),
            col("hostname"),
            col("program_name")
        ).createOrReplaceTempView('tbmgs')

        df1 = spark.sql("""
            select id,tb1.*,tb2.*
            from tbmgs tb1
            join dfIsDecoder tb2 on 1=1 
            """)

        
        # 应用UDF并展开结果字段
        df2 = df1.withColumn(
            "decoder_result",  # 临时存储UDF返回的结构体
            program_name_pcre2_spark_udf(
                col("program_name_pcre2"),
                col("parent"),
                col("program_name_flag"),
                col("processed_msg"),
                col("program_name")
            )
        ).select(
            # 保留原始列
            "*",
            # 展开结构体中的OK和msg字段
            col("decoder_result.OK").alias("OK"),
            col("decoder_result.msg").alias("msg")
        ).where(col("OK")).drop("decoder_result","OK")
        # df2.show()

        
        # 应用UDF并展开结果字段
        # msg,offset_in_prematch_pcre2,parent,prematch_pcre2,decoder_name
        df3 = df2.withColumn(
            "decoder_result",  # 临时存储UDF返回的结构体
            prematch_pcre2_spark_udf(
                col("msg"),
                col("offset_in_prematch_pcre2"),
                col("parent"),
                col("prematch_pcre2"),
                col("decoder_name")
            )
        ).select(
            # 保留原始列
            "*",
            # 展开结构体中的OK和msg字段
            col("decoder_result.OK").alias("OK"),
            col("decoder_result.span_start").alias("span_start"),
            col("decoder_result.span_end").alias("span_end")
        ).where(col("OK")).drop("decoder_result","OK")



        df3.groupBy("id").agg(
            collect_list(col("decoder_name")).alias("decoder"),
            collect_list(col("type")).alias("type")
        ).createOrReplaceTempView('tbdecoder')


        df_decoder2 =  spark.sql("""
        select *
                  from tbmgs tb1
                  join tbdecoder tb2 on tb1.id = tb2.id
        """)

        df_decoder2.show()



        spark.stop()



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

    o = OSSEC(msglist)
  
   