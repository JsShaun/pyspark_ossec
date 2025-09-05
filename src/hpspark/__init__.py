from pyspark.sql import SparkSession
from pyspark.sql.functions import broadcast
# from .msg import message_udf # 示例pandas_udf使用
# from .msgevent import envent_udf





class NewSpark:

    def __init__(self,url,name):
        "sc://localhost:15002"
        self.spark = SparkSession.builder.remote(url).appName(name).getOrCreate()
        
    def get_spark(self):
        "注册自定义udf"
        # self.spark.udf.register("message_udf",message_udf)
        # self.spark.udf.register("envent_udf",envent_udf)
        return self.spark
        



