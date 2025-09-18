# PySpark OSSEC 开发

### Python开发环境（虚拟环境）

- python3.10 -m venv .env
- source .env/bin/activate


# PySpark环境
## 安装兼容组合（重点确保 grpcio-status ≥1.48.1）
- pip3 install protobuf==6.32
- pip3 install grpcio==1.74
- pip3 install grpcio-status==1.74
- pip3 install googleapis-common-protos

## 安装开发需求库
- pip3 install pyspark==3.5.6
- pip3 install pandas
- pip3 install pyarrow
- pip3 install confluent-kafka
```confluent-kafka底层基于C语言实现，高效率运行```


## 项目说明
    1、pyspark 是