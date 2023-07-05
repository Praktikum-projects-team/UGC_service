from kafka import KafkaConsumer
from config import etl_config
from typing import Optional
import json

consumer: Optional[KafkaConsumer] = None


def extract_data():
    events = []
    for message in consumer:
        events.append(json.loads(message.value))
        if len(events) >= etl_config.kafka_data_size:
            return events
