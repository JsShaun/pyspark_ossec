# pyspark_ossec


### python虚拟环境
- python3.10 -m venv .env
- source .env/bin/activate


# PySpark应用
## 先卸载所有相关包以避免残留
- pip3 uninstall -y protobuf grpcio grpcio-status googleapis-common-protos

## 安装兼容组合（重点确保 grpcio-status ≥1.48.1）
- pip3 install protobuf==6.32
- pip3 install grpcio==1.74
- pip3 install grpcio-status==1.74
- pip3 install googleapis-common-protos

## 安装pyspark库
- pip3 install pyspark==3.5.6
- pip3 install pandas
- pip3 install pyarrow

### 底层基于C语言实现，高效率
- pip3 install confluent-kafka
