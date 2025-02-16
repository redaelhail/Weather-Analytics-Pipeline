# Weather Analytics Pipeline - Kafka Producer & Consumer

This project generates synthetic weather data and streams it to a Kafka topic in Confluent Cloud using the Kafka Producer API in Python. The weather data, including readings such as temperature, humidity, and wind speed, is sent to the Kafka topic. Consumers (running in Databricks notebooks) can then process this data in real-time for analysis or visualization.

## Project Overview

The Weather Analytics Pipeline simulates weather data, creates JSON payloads with sensor data, and sends them to the Kafka topic in Confluent Cloud. The consumer notebooks in Databricks consume this data for further processing, such as analytics, data visualization, or storing it in a database for further use.

## Prerequisites

Before running the producer or consumer, you need the following:

A Confluent Cloud account (Sign up at Confluent Cloud).
A Kafka Cluster set up in Confluent Cloud.
An API Key and API Secret for accessing your Kafka cluster.
Python 3.6+ installed on your machine for the producer.
Databricks account and a Databricks cluster for the consumer notebooks.
Kafka Python library installed for running the producer locally.
Installation

1. Install Python and Dependencies for Producer
Ensure that you have Python 3.6 or higher installed on your system. You can install the necessary dependencies using pip:

        pip install kafka-python

2. Get Confluent Cloud Details
Bootstrap Servers: Obtain the Kafka broker endpoint (Bootstrap Server) from your Confluent Cloud console.
API Key and Secret: Create an API key in the Confluent Cloud console under the API Keys section and assign it the necessary permissions to produce messages to your Kafka topic.
3. Set Up Your Confluent Cloud Kafka Cluster
If you don't have a Kafka cluster in Confluent Cloud, follow these steps to create one:

   1.Log in to Confluent Cloud.
   
   2.Create a new Kafka Cluster.

   3.Go to the API Keys section to generate a new API Key and API Secret.

## Usage

1. Configure the Producer Script
In the weather_producer.py file, replace the following values with your own:

- <API_KEY>: Replace with your Confluent Cloud API Key.
- <API_SECRET>: Replace with your Confluent Cloud API Secret.
- bootstrap_servers: Replace with the correct Kafka broker endpoint from your Confluent Cloud console.

Here’s the configuration section for reference:
        
        producer = KafkaProducer(
            bootstrap_servers=['pkc-xxxxxx.us-east-1.aws.confluent.cloud:9092'],  # Your Kafka broker URL
            security_protocol='SASL_SSL',
            sasl_mechanism='PLAIN',
            sasl_plain_username='<API_KEY>',  # Replace with your API key
            sasl_plain_password='<API_SECRET>',  # Replace with your API secret
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )
2. Run the Producer
Once the script is configured, run it locally to start producing synthetic weather data to your Confluent Cloud Kafka topic:

        python weather_producer.py

This will continuously send synthetic weather readings (temperature, humidity, wind speed) every second to the weather-readings Kafka topic in Confluent Cloud.

3. Monitor the Output
Once the producer is running, you should see the following output:

        Sent: {'sensor_id': 'sensor-1', 'temperature': 20.54, 'humidity': 45.67, 'wind_speed': 12.3, 'timestamp': '2025-02-16T10:05:30.567'}
        Sent: {'sensor_id': 'sensor-2', 'temperature': 18.12, 'humidity': 48.22, 'wind_speed': 15.7, 'timestamp': '2025-02-16T10:05:31.567'}
        ...
4. Databricks Consumer Setup
In your Databricks notebook, you can use PySpark to consume the weather data from your Kafka topic.

Databricks Notebook Code Example:

    from pyspark.sql import SparkSession
    from pyspark.sql.functions import expr
    
    # Initialize Spark Session
    spark = SparkSession.builder.appName("WeatherConsumer").getOrCreate()
    
    # Confluent Cloud Kafka broker details
    bootstrap_servers = "pkc-xxxxxx.us-east-1.aws.confluent.cloud:9092"
    api_key = "<API_KEY>"
    api_secret = "<API_SECRET>"
    
    # Kafka Options
    kafka_options = {
        "kafka.bootstrap.servers": bootstrap_servers,
        "subscribe": "weather-readings",
        "kafka.sasl.jaas.config": f"org.apache.kafka.common.security.plain.PlainLoginModule required username='{api_key}' password='{api_secret}';",
        "kafka.security.protocol": "SASL_SSL",
        "kafka.sasl.mechanism": "PLAIN",
        "startingOffsets": "earliest"
    }

    # Read from Kafka
    weather_data = spark.readStream.format("kafka").options(**kafka_options).load()
    
    # Convert the value column from Kafka (which is in binary) to a string
    weather_data_df = weather_data.selectExpr("CAST(value AS STRING)")
    
    # Parse the JSON and create columns for weather readings
    weather_data_df = weather_data_df.selectExpr("json_tuple(value, 'sensor_id', 'temperature', 'humidity', 'wind_speed', 'timestamp') as (sensor_id, temperature, humidity, wind_speed, timestamp)")
    
    # Write the data to the console
    query = weather_data_df.writeStream.outputMode("append").format("console").start()
    
    query.awaitTermination()
This will allow you to consume the data produced by your weather producer from the Kafka topic and process it in real-time within your Databricks notebook.
# Directory Structure 👀

    weather-analytics/
    ├── producer/                     
    │   ├── weather_producer.py
    │   ├── config.py
    │   └── requirements.txt
    ├── databricks/                   
    │   ├── 01_kafka_setup.ipynb
    │   ├── 02_streaming_pipeline.ipynb
    │   └── 03_analytics_dashboard.ipynb
    ├── config/                        
    │   ├── kafka_config.json
    │   └── spark_config.json
    ├── requirements.txt
    └── README.md
