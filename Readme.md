# Spark Streaming with Real-Time Data and Kafka

This project demonstrates the implementation of a Spark Streaming application that continuously reads text data from a real-time source, analyzes the text for named entities, and sends their counts to Apache Kafka. Additionally, it involves a pipeline that uses Elasticsearch and Kibana to visualize the data retrieved from Kafka.

## Setting up Your Development Environment

To set up your development environment, you'll need the following resources:

- Access to a real-time text data source such as Reddit, NewsAPI, or Finnhub.
- Apache Kafka. Follow the quickstart steps: [Kafka Quickstart](https://kafka.apache.org/quickstart)
- A working Spark cluster, either locally or on a cloud-based server.
- Elasticsearch, Kibana, and Logstash. Download them from [Elastic](https://www.elastic.co/downloads/).

For Windows users, consider using WSL to create a Unix-like environment: [WSL Installation Guide](https://docs.microsoft.com/en-us/windows/wsl/install-win10).

## Project Steps

1. **Data Source Setup**: Create a Python application to read from a real-time data source. Use libraries like PRAW for Reddit, NewsAPI, or Finnhub for financial news.

2. **Data Streaming to Kafka**: Continuously write incoming data to a Kafka topic (e.g., `topic1`).

3. **Spark Structured Streaming**: Develop a PySpark structured streaming application to read data from Kafka (`topic1`). Keep a running count of named entities mentioned in the text.

4. **Message Publication to Another Kafka Topic**: At the trigger time, send a message containing the named entities and their counts to another Kafka topic (e.g., `topic2`).

5. **Elasticsearch, Logstash, and Kibana Configuration**: Configure Logstash, Elasticsearch, and Kibana to read from `topic2`. Create a bar plot visualization of the top 10 most frequent named entities and their counts.

## Visualizing Data using Elasticsearch and Kibana

Ensure Elasticsearch and Kibana are installed to visualize data from Kafka. Follow the installation guides:

- [Elasticsearch Downloads](https://www.elastic.co/downloads)
- [Kibana Downloads](https://www.elastic.co/start)

Visualize the top 10 named entities mentioned in your chosen data source using a bar plot in Kibana.
