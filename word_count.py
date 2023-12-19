import json

import nltk
import pyspark
from kafka import KafkaProducer
from nltk import Tree
from nltk import word_tokenize, pos_tag, ne_chunk
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.types import StringType, ArrayType

from constants import bootstrap_servers, reddit_topic, elk_topic

# NLTK Downloads
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

# Spark initialization
spark = SparkSession \
    .builder \
    .appName("StructuredKafkaWordCount") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# Read data from reddit topic
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", bootstrap_servers) \
    .option('subscribe', reddit_topic) \
    .load() \
    .selectExpr("CAST(value AS STRING) AS text")


# Define UDF to extract named entities
def extract_named_entities(text):
    words = word_tokenize(text)
    pos_tags = pos_tag(words)
    named_entities = ne_chunk(pos_tags)
    ans = []
    for chunk in named_entities:
        if isinstance(chunk, Tree) and hasattr(chunk, 'label'):
            term = ' '.join([w for w, _ in chunk.leaves()])
            named_entity_category = chunk.label()
            ans.append(term)
    return ans


# Define UDF and specify return type as ArrayType(StringType())
extract_named_entities_udf = spark.udf.register("extract_named_entities", extract_named_entities,
                                                ArrayType(StringType()))

# Apply the NER extraction UDF
df = df.withColumn("named_entities", explode(extract_named_entities_udf("text")))

# Count the occurrences of each named entity
named_entities_count = df.groupBy("named_entities").count()


# Create a function to push Structured Stream data to kafka topic in mini-batch mode.
def send_data_to_kafka(row: pyspark.Row):
    elk_producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
    key = row['named_entities']
    value = json.dumps(row.asDict())
    elk_producer.send(elk_topic, key=key.encode(), value=value.encode())


# Mini-batch processing of the stream
write_query = named_entities_count.writeStream \
    .outputMode("complete") \
    .foreach(send_data_to_kafka) \
    .start()

# Outputting data to console for examination.
query = named_entities_count \
    .writeStream \
    .outputMode('complete') \
    .format('console') \
    .start()

write_query.awaitTermination()
query.awaitTermination()

# Command to run word_count.py
# spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1 word_count.py
