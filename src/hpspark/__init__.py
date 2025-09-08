from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType
from .polars_udf import *
from .pandas_udfs import *




class NewSpark:

    def __init__(self,url="sc://localhost:15002",name="AppTest"):
        
        self.spark = SparkSession.builder.remote(url).appName(name).getOrCreate()

        
    def get_spark(self):
        
        "注册自定义udf"
        self.spark.udf.register("message_udf",message_udf)
        self.spark.udf.register("envent_udf",envent_udf)
        self.spark.udf.register("polars_func",polars_func)

        return self.spark
        


    
            