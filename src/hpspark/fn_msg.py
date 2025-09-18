from pyspark.sql.functions import pandas_udf
from pyspark.sql.types import StructType, StructField, StringType, BooleanType
import pandas as pd


result_schema = StructType([
    StructField("original_msg", StringType()),
    StructField("full_event", StringType()),
    StructField("processed_msg", StringType()),
    StructField("hostname", StringType()),
    StructField("program_name", StringType()),
])

@pandas_udf(result_schema)
def message_udf(msg:pd.Series) -> pd.DataFrame:
    '''返回多字段'''
    full_event = msg.str.replace(r"\s+", " ",regex=True)
    # 2. 移除不同格式的日期时间
    # 格式1: [Mon. Jan. 1 00:00:00 2023] 
    date_pattern1 = r"^\[(Mond?a?y?|Tues?d?a?y?|Wedn?e?s?d?a?y?|Thur?s?d?a?y?|Frid?a?y?|Satu?r?d?a?y?|Sund?a?y?)\.? (Janu?a?r?y?|Febr?u?a?r?y?|Marc?h?|Apri?l?|May|June?|July?|Augu?s?t?|Sept?e?m?b?e?r?|Octo?b?e?r?|Nove?m?b?e?r?|Dece?m?b?e?r?)\.? {1,2}\d{1,2} {1,2}\d{1,2}:\d{1,2}:\d{1,2} \d{4}\] ?"
    # 格式2: Jan 1 00:00:00 
    date_pattern2 = r"^(Janu?a?r?y?|Febr?u?a?r?y?|Marc?h?|Apri?l?|May|June?|July?|Augu?s?t?|Sept?e?m?b?e?r?|Octo?b?e?r?|Nove?m?b?e?r?|Dece?m?b?e?r?)\.? {1,2}(\d{1,2}) {1,2}(\d{1,2}:\d{1,2}:\d{1,2}) "
    # 格式3: 2023-1-1 00:00:00 或 2023-01-01T00:00:00+08:00
    date_pattern3 = r"^\d{4}-\d{1,2}-\d{1,2}(T| )(\d{1,2}:\d{1,2}:\d{2})(\S)+ "
    processed_msg = full_event.str.replace(date_pattern1,"",regex=True).replace(date_pattern2,"",regex=True).replace(date_pattern3,"",regex=True)
    # 3. 提取hostname
    hostname_pattern = r"^([^\f\n\r\t\v:]+) "
    hostname = processed_msg.str.extract(hostname_pattern,expand=False)

    program_name_pattern = r"^.*?\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\s+(\w+)(?=\[)"
    program_name = msg.str.extract(program_name_pattern, expand=False)

    return pd.DataFrame({
        "original_msg": msg,
        "full_event": full_event,
        "processed_msg": processed_msg,
        "hostname": hostname,
        "program_name": program_name,
    })




@pandas_udf(BooleanType())
def envent_udf(original_msg:pd.Series) -> pd.Series:
    '''返回单字段'''
    return original_msg == original_msg