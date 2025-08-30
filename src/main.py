import warnings
warnings.filterwarnings('ignore')
import numpy as np
from sys import getsizeof
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import regexp_replace, regexp_extract, col, collect_list, when, udf, pandas_udf
from pyspark.sql.types import StructType, StructField, StringType, ArrayType, BooleanType, IntegerType, MapType
import pandas as pd
import re
# 假设这两个模块存在
from regular.decoder import get_decoder_dataframe  # 返回pandas DataFrame
from regular.rules import get_rules_dataframe      # 返回pandas DataFrame


spark = SparkSession.builder \
    .remote("sc://localhost:15002") \
    .appName("CreateDataFrameWithPolars") \
    .getOrCreate()


# 定义返回类型结构（包含OK和msg两个字段）
result_schema = StructType([
    StructField("OK", BooleanType()),  # 明确指定不可为空
    StructField("msg", StringType())
])

@pandas_udf(result_schema)
def program_name_pcre2_udf(parent: pd.Series) -> pd.DataFrame:
    """Pandas UDF实现，返回与输入长度匹配的结果"""
    
    # 关键修复：确保OK字段不可为空（通过设置dtype和不包含空值）
    flags = pd.Series([True] * len(parent), name="OK", dtype=bool)
    # 确保没有空值（如果有条件判断，需要处理可能产生的空值）
    flags = flags.fillna(False)  # 即使有null也替换为False，保证非空
    
    cleaned_logs = pd.Series([""] * len(parent), name="msg")
    
    # 构建DataFrame时再次确认字段非空
    result_df = pd.DataFrame({
        "OK": flags,
        "msg": cleaned_logs
    })
    
    # 额外验证：确保OK列没有空值
    assert not result_df["OK"].isnull().any(), "OK字段包含空值，违反schema定义"
    return result_df


class OSSEC:
    def __init__(self, msglist: list):
        # 使用全局spark会话
        self.spark = spark
        
        # 注册UDF
        self.spark.udf.register("program_name_pcre2_udf2", program_name_pcre2_udf)
        
        # 获取数据并创建视图
        df_decoder = get_decoder_dataframe()
        self.spark.createDataFrame(df_decoder).createOrReplaceTempView('dfIsDecoder')
        
        # 执行查询，明确提取UDF返回的字段
        df1 = self.spark.sql("""
            select 
                tb1.*,
                program_name_pcre2_udf2(tb1.parent).OK as ok_flag,
                program_name_pcre2_udf2(tb1.parent).msg as message
            from dfIsDecoder tb1
        """)
        
        df1.show()


if __name__ == "__main__":
    msg1 = """Jun 25 14:04:30 10.0.0.1 dropbear[30746]: Failed listening on '7001': Error listening: Address already in use""" 
    msg2 = """May  8 08:26:55 mail postfix/postscreen[22055]: NOQUEUE: reject: RCPT from [157.122.148.242]:47407: 550 5.7.1 Service unavailable; client [157.122.148.242] blocked using bl.spamcop.net; from=<kos@mafia.network>, to=<z13699753428@vip.163.com>, proto=ESMTP, helo=<XL-20160217QQJV>""" 
    
    msglist = [
        {'msg': msg1, 'id': 1},
        {'msg': msg2, 'id': 2}
    ]

    o = OSSEC(msglist)
    # 程序结束时停止Spark会话
    spark.stop()
    