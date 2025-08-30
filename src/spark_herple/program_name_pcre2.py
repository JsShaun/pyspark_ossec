from pyspark.sql.functions import regexp_replace,regexp_extract,col,collect_list,when,udf,pandas_udf
from pyspark.sql.types import StructType, StructField, StringType, ArrayType, BooleanType, IntegerType, MapType
import re
import pandas as pd


# 定义返回类型结构（包含OK和msg两个字段）
result_schema = StructType([
    StructField("OK", BooleanType()),  # 明确指定不可为空
    StructField("msg", StringType())
])

@pandas_udf(result_schema)
def program_name_pcre2_udf(program_name_pcre2:pd.Series, parent:pd.Series, program_name_flag:pd.Series, processed_msg:pd.Series, program_name:pd.Series):

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