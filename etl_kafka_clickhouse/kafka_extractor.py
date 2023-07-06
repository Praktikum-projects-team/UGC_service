from config import etl_config
import json


def extract_data(consumer):
    events = []
    for message in consumer:
        events.append(json.loads(message.value))
        if len(events) >= etl_config.kafka_data_size:
            return events
