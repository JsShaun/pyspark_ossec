from pyspark.sql.functions import regexp_replace,regexp_extract,col,collect_list,when,udf
from pyspark.sql.types import StructType, StructField, StringType, ArrayType, BooleanType, IntegerType, MapType
import re




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