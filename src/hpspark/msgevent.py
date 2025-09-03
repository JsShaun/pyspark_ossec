from pyspark.sql.functions import pandas_udf
from pyspark.sql.types import BooleanType
import pandas as pd



@pandas_udf(BooleanType())
def envent_udf(original_msg:pd.Series) -> pd.Series:
    return original_msg
