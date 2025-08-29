import warnings
warnings.filterwarnings('ignore')
import re
from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_replace, regexp_extract, col, collect_list, when, udf
from pyspark.sql.types import StructType, StructField, StringType, ArrayType, BooleanType, IntegerType
import pandas as pd
from regular.decoder import get_decoder_dataframe
from regular.rules import get_rules_dataframe


# ------------------------------
# 1. 初始化SparkSession（单例模式）
# ------------------------------
def create_spark_session() -> SparkSession:
    """创建配置优化的SparkSession，避免重复初始化"""
    return SparkSession.builder \
        .remote("sc://localhost:15002") \
        .appName("OSSECLogProcessor") \
        .getOrCreate()


# ------------------------------
# 2. UDF定义与注册（集中管理）
# ------------------------------
# 2.1 program_name_pcre2 UDF
program_name_result_schema = StructType([
    StructField("OK", BooleanType(), nullable=False),
    StructField("msg", StringType(), nullable=True)
])

def _program_name_pcre2_udf(program_name_pcre2, parent, program_name_flag, processed_msg, program_name):
    """匹配程序名正则并清理日志前缀"""
    # 空值防御
    if not all([program_name_pcre2, processed_msg, program_name]):
        return (False, "Missing required parameters")
    
    try:
        # 预编译正则（过滤空模式）
        patterns = [
            re.compile(pattern.strip(), re.IGNORECASE) 
            for pattern in program_name_pcre2 
            if pattern and isinstance(pattern, str)
        ]
    except re.error as e:
        return (False, f"Regex error: {str(e)}")

    if parent == "":
        # 遍历正则匹配
        for pattern in patterns:
            if pattern.search(program_name):
                cleaned_log = re.sub(r"^(\S+): ", "", processed_msg)
                return (True, cleaned_log)
            return (False, "No match in patterns")  # 第一个不匹配即返回

        # 无匹配时根据flag处理
        if program_name_flag:
            cleaned_log = re.sub(r"^(\S+): ", "", processed_msg)
            return (True, cleaned_log)
        return (True, processed_msg)
    
    return (False, "Parent is not empty")

program_name_pcre2_spark_udf = udf(_program_name_pcre2_udf, program_name_result_schema)


# 2.2 prematch_pcre2 UDF
prematch_result_schema = StructType([
    StructField("OK", BooleanType(), nullable=False),
    StructField("span_start", IntegerType(), nullable=True),
    StructField("span_end", IntegerType(), nullable=True)
])

def _prematch_pcre2_udf(msg, offset_in_prematch_pcre2, parent, prematch_pcre2, decoder_name):
    """prematch正则判定及字符剔除"""
    if not all([msg, offset_in_prematch_pcre2, prematch_pcre2]):
        return (False, 0, 0)

    span_start, span_end = 0, 0
    current_msg = msg  # 避免修改原始消息

    # 处理after_parent逻辑
    if "after_parent" in offset_in_prematch_pcre2 and decoder_name == parent:
        # 这里补充原逻辑中缺失的span处理（根据实际业务完善）
        pass

    # 正则匹配处理
    for pattern_str in prematch_pcre2:
        if not pattern_str or not isinstance(pattern_str, str):
            continue
        try:
            pattern = re.compile(pattern_str.strip(), re.IGNORECASE)
            mobj = pattern.search(current_msg)
        except re.error:
            return (False, 0, 0)

        if mobj and mobj.group() != "":
            span_end += mobj.span()[1]
            return (True, span_start, span_end)
        return (False, 0, 0)  # 第一个不匹配即返回

    return (True, None, None)

prematch_pcre2_spark_udf = udf(_prematch_pcre2_udf, prematch_result_schema)


# 2.3 pcre2 UDF
pcre2_result_schema = StructType([
    StructField("OK", BooleanType(), nullable=False),
    StructField("shijian", StringType(), nullable=False),
])

def _pcre2_udf(msg, offset_in_pcre2, decoder_name, parent, span_start, span_end, pcre2, order):
    """pcre2正则提取字段值"""
    if not all([msg, pcre2, order]):
        return (False, "{}")

    current_msg = msg

    # 处理offset逻辑
    if "after_parent" in offset_in_pcre2 and decoder_name == parent and span_end:
        current_msg = current_msg[span_end:]
    if "after_prematch" in offset_in_pcre2 and span_start is not None:
        current_msg = current_msg[span_start:]
    if "after_regex" in offset_in_pcre2:
        for pattern_str in pcre2:
            if pattern_str and isinstance(pattern_str, str):
                try:
                    current_msg = re.compile(pattern_str, re.IGNORECASE).sub("", current_msg)
                except re.error:
                    continue

    # 提取并处理匹配结果
    for pattern_str in pcre2:
        if not pattern_str or not isinstance(pattern_str, str):
            continue
        try:
            matches = re.compile(pattern_str, re.IGNORECASE).findall(current_msg)
        except re.error:
            continue

        # 展平列表并过滤空值（纯Python实现）
        flat_list = []
        for item in matches:
            if isinstance(item, tuple):
                flat_list.extend(item)
            else:
                flat_list.append(item)
        filtered_list = [x for x in flat_list if x != ""]

        if filtered_list:
            # 确保order和结果长度匹配
            result_dict = dict(zip(order[:len(filtered_list)], filtered_list))
            return (True, str(result_dict))

    return (False, "{}")

pcre2_spark_udf = udf(_pcre2_udf, pcre2_result_schema)


# ------------------------------
# 3. 主处理类（职责单一化）
# ------------------------------
class OSSEC:
    def __init__(self, msglist: list):
        self.spark = create_spark_session()
        try:
            self.process(msglist)
        finally:
            self.spark.stop()  # 确保资源释放

    def process(self, msglist: list):
        """主处理流程"""
        # 加载解码器数据
        self._load_decoder_data()
        
        # 日志预处理
        preprocessed_df = self._preprocess_logs(msglist)
        
        # 执行解码流程
        result_df = self._decode_logs(preprocessed_df)
        
        # 展示结果
        self._display_results(result_df)

    def _load_decoder_data(self):
        """加载并注册解码器数据视图"""
        df_decoder = get_decoder_dataframe()
        # 确保关键列类型正确
        if "program_name_pcre2" in df_decoder.columns:
            df_decoder["program_name_pcre2"] = df_decoder["program_name_pcre2"].apply(
                lambda x: x if isinstance(x, list) else [] if pd.isna(x) else [x]
            )
        self.spark.createDataFrame(df_decoder).createOrReplaceTempView('dfIsDecoder')

    def _preprocess_logs(self, msglist: list):
        """日志预处理：清洗、提取基础字段"""
        df = self.spark.createDataFrame(msglist)
        
        # 1. 替换多个空格为单个空格
        df = df.withColumn("full_event", regexp_replace(col("msg"), r"\s+", " ")) \
               .withColumn("processed_msg", col("full_event"))

        # 2. 移除日期时间（合并正则减少操作）
        date_patterns = "|".join([
            r"^\[(Mond?a?y?|Tues?d?a?y?|Wedn?e?s?d?a?y?|Thur?s?d?a?y?|Frid?a?y?|Satu?r?d?a?y?|Sund?a?y?)\.? (Janu?a?r?y?|Febr?u?a?r?y?|Marc?h?|Apri?l?|May|June?|July?|Augu?s?t?|Sept?e?m?b?e?r?|Octo?b?e?r?|Nove?m?b?e?r?|Dece?m?b?e?r?)\.? {1,2}\d{1,2} {1,2}\d{1,2}:\d{1,2}:\d{1,2} \d{4}\] ?",
            r"^(Janu?a?r?y?|Febr?u?a?r?y?|Marc?h?|Apri?l?|May|June?|July?|Augu?s?t?|Sept?e?m?b?e?r?|Octo?b?e?r?|Nove?m?b?e?r?|Dece?m?b?e?r?)\.? {1,2}(\d{1,2}) {1,2}(\d{1,2}:\d{1,2}:\d{1,2}) ",
            r"^\d{4}-\d{1,2}-\d{1,2}(T| )(\d{1,2}:\d{1,2}:\d{2})(\S)+ "
        ])
        df = df.withColumn("processed_msg", regexp_replace(col("processed_msg"), date_patterns, ""))

        # 3. 提取hostname和程序名
        df = df.withColumn("hostname", regexp_extract(col("processed_msg"), r"^([^\f\n\r\t\v:]+) ", 1)) \
               .withColumn("program_match1", regexp_extract(col("processed_msg"), r"^([^\f\n\r\t\v:]+ )?([^\f\n\r\t\v:]+\[\S+\]:? )", 0)) \
               .withColumn("program_part1", regexp_extract(col("processed_msg"), r"^([^\f\n\r\t\v:]+ )?([^\f\n\r\t\v:]+\[\S+\]:? )", 2)) \
               .withColumn("program_match2", regexp_extract(col("processed_msg"), r"^([^\f\n\r\t\v:]+ )?([^\[\]\f\n\r\t\v]+: )", 0)) \
               .withColumn("program_part2", regexp_extract(col("processed_msg"), r"^([^\f\n\r\t\v:]+ )?([^\[\]\f\n\r\t\v]+: )", 2))

        # 合并程序名匹配结果
        df = df.withColumn("program_match", when(col("program_match1") == "", col("program_match2")).otherwise(col("program_match1"))) \
               .withColumn("program_part", when(col("program_part1") == "", col("program_part2")).otherwise(col("program_part1"))) \
               .withColumn("formatted_program", regexp_replace(col("program_part"), r"(\[\S+\])?:? ", ": ")) \
               .withColumn("processed_msg", regexp_replace(col("processed_msg"), col("program_match"), col("formatted_program"))) \
               .withColumn("program_name", regexp_extract(col("formatted_program"), r"^(\S+): ?", 1))

        # 4. 替换大括号为引号
        df = df.withColumn("processed_msg", regexp_replace(col("processed_msg"), r"\{", '"')) \
               .withColumn("processed_msg", regexp_replace(col("processed_msg"), r"\}", '"'))

        # 选择需要的列并注册视图
        result_df = df.select(
            col("id"),
            col("msg").alias("original_msg"),
            col("full_event"),
            col("processed_msg"),
            col("hostname"),
            col("program_name")
        )
        result_df.createOrReplaceTempView('tbmgs')
        return result_df

    def _decode_logs(self, preprocessed_df):
        """执行解码流程：关联解码器 + 应用UDF"""
        # 1. 关联解码器数据（笛卡尔积，建议后续优化为有条件关联）
        joined_df = self.spark.sql("""
            SELECT id, tb1.*, tb2.*
            FROM tbmgs tb1
            JOIN dfIsDecoder tb2 ON 1=1
        """)

        # 2. 应用program_name_pcre2 UDF
        df_program = joined_df.withColumn(
            "program_result",
            program_name_pcre2_spark_udf(
                col("program_name_pcre2"),
                col("parent"),
                col("program_name_flag"),
                col("processed_msg"),
                col("program_name")
            )
        ).select(
            "*",
            col("program_result.OK").alias("program_OK"),
            col("program_result.msg").alias("program_msg")
        ).where(col("program_OK")).drop("program_result", "program_OK")

        # 3. 应用prematch_pcre2 UDF
        df_prematch = df_program.withColumn(
            "prematch_result",
            prematch_pcre2_spark_udf(
                col("program_msg"),
                col("offset_in_prematch_pcre2"),
                col("parent"),
                col("prematch_pcre2"),
                col("decoder_name")
            )
        ).select(
            "*",
            col("prematch_result.OK").alias("prematch_OK"),
            col("prematch_result.span_start").alias("span_start"),
            col("prematch_result.span_end").alias("span_end")
        ).where(col("prematch_OK")).drop("prematch_result", "prematch_OK")

        # 4. 聚合解码器结果（按id分组）
        df_aggregated = df_prematch.groupBy("id") \
            .agg(
                collect_list(col("decoder_name")).alias("decoder_list"),
                collect_list(col("type")).alias("type_list")
            )

        # 5. 关联回原始日志数据
        return self.spark.sql("""
            SELECT tb1.*, tb2.decoder_list, tb2.type_list
            FROM tbmgs tb1
            JOIN (SELECT * FROM df_aggregated) tb2
            ON tb1.id = tb2.id
        """)

    def _display_results(self, df):
        """展示处理结果"""
        print("\n=== 日志解码结果 ===")
        df.select("id", "original_msg", "decoder_list", "type_list").show(truncate=100)


# ------------------------------
# 4. 入口函数
# ------------------------------
if __name__ == "__main__":
    # 测试数据
    msg1 = """Jun 25 14:04:30 10.0.0.1 dropbear[30746]: Failed listening on '7001': Error listening: Address already in use"""
    msg2 = """May  8 08:26:55 mail postfix/postscreen[22055]: NOQUEUE: reject: RCPT from [157.122.148.242]:47407: 550 5.7.1 Service unavailable; client [157.122.148.242] blocked using bl.spamcop.net; from=<kos@mafia.network>, to=<z13699753428@vip.163.com>, proto=ESMTP, helo=<XL-20160217QQJV>"""
    
    msglist = [{'msg': msg1, 'id': 1}, {'msg': msg2, 'id': 2}]
    OSSEC(msglist)
