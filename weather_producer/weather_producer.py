from kafka import KafkaProducer
import json
import time
import random
from datetime import datetime
import yaml

def create_weather_reading():
    """Generate synthetic weather sensor data"""
    sensors = ['sensor-1', 'sensor-2', 'sensor-3', 'sensor-4']
    weather_data = {
        'sensor_id': random.choice(sensors),
        'temperature': round(random.uniform(-5, 35), 2),
        'humidity': round(random.uniform(30, 90), 2),
        'wind_speed': round(random.uniform(0, 100), 2),
        'timestamp': datetime.now().isoformat()
    }
    return weather_data

def main():
    config = yaml.load('config.yml')

    # Replace with your Confluent Cloud Kafka cluster details
    bootstrap_servers = [config['confluent']['bootstrap_servers']]  # e.g. 'pkc-xxxxxx.us-east-1.aws.confluent.cloud:9092'
    api_key = config['confluent']['api_key']
    api_secret = config['confluent']['api_secret']

    producer = KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        security_protocol='SASL_SSL',
        sasl_mechanism='PLAIN',
        sasl_plain_username=api_key,
        sasl_plain_password=api_secret,
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )
    
    while True:
        weather_reading = create_weather_reading()
        producer.send('weather-readings', weather_reading)
        print(f"Sent: {weather_reading}")
        time.sleep(15)

if __name__ == "__main__":
    main()
