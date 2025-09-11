# 基于官方Spark 3.5.6镜像
FROM apache/spark:4.0.0

USER root

RUN pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip3 config set global.trusted-host pypi.tuna.tsinghua.edu.cn

RUN pip3 install --no-cache-dir \
    pandas \
    pyarrow 