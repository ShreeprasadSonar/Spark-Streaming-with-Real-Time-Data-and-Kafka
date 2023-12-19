Initial Setup

1. Start ZooKeeper
> cd /usr/local/Cellar/kafka/3.6.0/libexec
> bin/zookeeper-server-start.sh config/zookeeper.properties

2. Start Kafka
> bin/kafka-server-start.sh config/server.properties

3. Run reddit_stream.py to read reddit comments and push data to reddit kafka topic. You would need an active reddit
   account and create an app on reddit account. Please follow https://praw.readthedocs.io/en/latest/getting_started/quick_start.html
   for the steps. You need to update config.py with your configurations before runnning reddit_stream.py.
> python3 reddit_stream.py

4. Run word_count.py as a Spark job to read from reddit kafka topic and write to elk kafka topic
> spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1 word_count.py

The count of named entities are being pushed to 'elk' kafka topic

5. Start elasticsearch
> cd /usr/local/Cellar/elasticsearch-full/7.17.4/libexec
> bin/elasticsearch

6. Start Kibana
> /usr/local/Cellar/kibana-full/7.17.4/libexec
> bin/kibana

7. Once Elasticsearch and Kibana are running, start logstash with a config file consuming data
   from 'elk' kafka topic and pushing to elasticsearch.
> cd /usr/local/Cellar/logstash/8.11.0/libexec
> bin/logstash -f logstash-config.conf

logstash-config.conf file is present in the files as well.