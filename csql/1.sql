
DROP TABLE IF EXISTS msg_event;
CREATE TABLE msg_event (
  original_msg String,
  hostname Nullable(String),
  program Nullable(String),
  event_cn Nullable(String),
  event_type Nullable(String),
  level Int8,
  level_cn Nullable(String),
  log_category Nullable(String),
  timestamp DateTime
) ENGINE = MergeTree()
ORDER BY (timestamp)
PARTITION BY toYYYYMM(timestamp)  -- 按“年月”分区（可选，推荐配置）
TTL timestamp + INTERVAL 360 DAY  -- 数据保留 90 天（可选）
SETTINGS index_granularity = 8192;  -- 索引粒度（默认 8192 行，控制索引精度）



