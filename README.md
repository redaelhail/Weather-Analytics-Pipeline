# Weather-Analytics-Pipeline
The project includes three main components:  A Kafka producer that generates synthetic weather data A Spark Structured Streaming pipeline for real-time processing An analytics dashboard for insights and monitoring

# Project Architecture 👀

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
