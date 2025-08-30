from pyspark.sql import SparkSession
# from .program_name_pcre2 import program_name_pcre2_udf
from .msg import message_udf





class NewSpark:

    def __init__(self,url,name):
        "sc://localhost:15002"
        self.spark = SparkSession.builder.remote(url).appName(name).getOrCreate()
        

    def get_spark(self):
        "注册自定义udf"
        # self.spark.udf.register("program_name_pcre2_udf",program_name_pcre2_udf)
        self.spark.udf.register("message_udf",message_udf)
        return self.spark
        



