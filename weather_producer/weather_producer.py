from kafka import KafkaProducer
import json
import time
import random
from datetime import datetime

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
    producer = KafkaProducer(
        bootstrap_servers=['127.0.0.1:9092'],
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )
    
    while True:
        weather_reading = create_weather_reading()
        producer.send('weather-readings', weather_reading)
        print(f"Sent: {weather_reading}")
        time.sleep(1)

if __name__ == "__main__":
    main()