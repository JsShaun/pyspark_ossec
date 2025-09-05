from pyspark.sql.functions import pandas_udf
from pyspark.sql.types import BooleanType
import pandas as pd
from clickhouse_driver import Client

# 1. 创建同步客户端（最常用）
client = Client(
    host="localhost",       # ClickHouse 服务地址（如远程机器填 IP）
    port=9000,              # 原生 TCP 端口（默认 9000，HTTP 端口 8123 需指定 protocol="http"）
    database="default",     # 目标数据库（默认 "default"）
    user="default",         # 用户名（默认 "default"）
    password="",            # 密码（默认空，若配置了密码需填写）
    settings={              # 可选：连接参数（如超时、压缩）
        "connect_timeout": 5,  # 连接超时时间（秒）
        "compression": "lz4"   # 启用压缩（减少网络传输，推荐）
    }
)

# 2. 验证连接（执行简单查询）
try:
    # 查询 ClickHouse 版本
    version = client.execute("SELECT version()")
    print("ClickHouse 版本:", version[0][0])  # 输出示例：23.10.3.5
except Exception as e:
    print("连接失败:", str(e))



@pandas_udf(BooleanType())
def envent_udf(original_msg:pd.Series) -> pd.Series:

    insert_sql = """INSERT INTO `default`.msg_event
    (original_msg, hostname, program, event_cn, event_type, `level`, level_cn, log_category, `timestamp`)
    VALUES(%(original_msg)s, %(hostname)s, %(program)s, %(event_cn)s, %(event_type)s, %(level)s, %(level_cn)s, %(log_category)s, %(timestamp)s);"""




    client.execute(insert_sql, batch_data)
    return original_msg
