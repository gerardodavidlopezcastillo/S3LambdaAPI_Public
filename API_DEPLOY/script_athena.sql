create external table channel_stats.st_youtube_stats(
Channel_name string,
Subscribers bigint,
Video_count bigint,
Total_Views bigint,
Createt_at string
)
ROW FORMAT SERDE 
  'org.apache.hadoop.hive.serde2.OpenCSVSerde' 
WITH SERDEPROPERTIES ( 
  'escapechar'='\\', 
  'quoteChar'='\"', 
  'separatorChar'=',') 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://gt-datalake-dev-us-east-2-508186271604-stage/'
TBLPROPERTIES (
  'skip.header.line.count'='1');