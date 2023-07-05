import logging

from kafka import KafkaConsumer
from clickhouse_driver import Client
import time
from config import etl_config
import kafka_extractor
from transformer import transform
import clickhouse_loader

logging.basicConfig(level=logging.INFO)


def connect():
    kafka_extractor.consumer = KafkaConsumer(etl_config.kafka_topic,
                                             bootstrap_servers=[etl_config.kafka],
                                             group_id=etl_config.kafka_group_id,
                                             # api_version=(0, 11, 5),
                                             auto_offset_reset='earliest')
    kafka_extractor.consumer.subscribe(etl_config.kafka_topic)
    clickhouse_loader.ch_client = Client(host=etl_config.clickhouse)


def load():
    while True:
        logging.info('starting etl')
        events = kafka_extractor.extract_data()
        transformed_data = transform(events, etl_config.kafka_topic)
        clickhouse_loader.load_data(transformed_data, 'movie_views')
        time.sleep(etl_config.repeat_time_in_seconds)


if __name__ == '__main__':
    connect()
    load()
