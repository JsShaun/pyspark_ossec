# 基于官方Spark 4.0.0镜像
FROM apache/spark:4.0.0

# 切换到root用户以获得安装权限
USER root

# 安装必要工具并导入缺失的GPG公钥
RUN apt-get update -y && \
    apt-get install -y gnupg2 && \
    # 导入缺失的公钥
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 6ED0E7B82643E131 && \
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 78DBA3BC47EF2265 && \
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 762F67A0B2C39DE4 && \
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys BDE6D2B9216EC7A8 && \
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 8E9F831205B4BA95 && \
    # 清理缓存
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 使用清华大学国内源
RUN echo "deb http://mirrors.tuna.tsinghua.edu.cn/debian/ stable main contrib non-free" > /etc/apt/sources.list && \
    echo "deb http://mirrors.tuna.tsinghua.edu.cn/debian/ stable-updates main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb http://mirrors.tuna.tsinghua.edu.cn/debian-security stable-security main contrib non-free" >> /etc/apt/sources.list

# 更新源并安装python3-pip
RUN apt-get update --fix-missing && \
    apt-get install -y --no-install-recommends python3-pip && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 配置pip使用国内镜像源
RUN pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/ && \
    pip3 config set install.trusted-host pypi.tuna.tsinghua.edu.cn

# 安装pandas和pyarrow
RUN pip3 install --no-cache-dir pandas pyarrow

# 切换回spark用户
USER 185

# 保持官方入口点
ENTRYPOINT ["/opt/entrypoint.sh"]
    