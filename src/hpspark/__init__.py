from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType
from .msgevent import envent_udf




class NewSpark:

    def __init__(self,url="sc://localhost:15002",name="AppTest"):
        self.spark = SparkSession.builder.remote(url).appName(name).getOrCreate()
        # self.spark = SparkSession.builder.appName("syslogProcessApp").master("local[*]").getOrCreate()
        # self.spark.sparkContext.addPyFile("helper.zip") 
        
    def get_spark(self):
        "注册自定义udf"
        # self.spark.udf.register("message_udf",message_udf)
        self.spark.udf.register("envent_udf",envent_udf)
        return self.spark
        


    
            