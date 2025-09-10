


- pip3 install pyarrow polars


```py

def polars_func(iterator):
    '''使用polars数据处理'''
    import polars as pl
    for batch in iterator:
        df = pl.from_arrow(batch)
        # 在这里写polars处理逻辑
        arrow_table = df.to_arrow()
        for sub_batch in arrow_table.to_batches():
            yield sub_batch


df = result_df.mapInArrow(polars_func,df.schema)
```