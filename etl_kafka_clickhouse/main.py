import logging

from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
from clickhouse_driver import Client
from clickhouse_driver.errors import NetworkError
import time
from config import etl_config
import kafka_extractor
from transformer import transform
import clickhouse_loader
import backoff as backoff

logging.basicConfig(level=logging.INFO)


@backoff.on_exception(backoff.expo, (NoBrokersAvailable, NetworkError))
def connect():
    kafka_consumer = KafkaConsumer(etl_config.kafka_topic,
                                   bootstrap_servers=[etl_config.kafka],
                                   group_id=etl_config.kafka_group_id,
                                   auto_offset_reset='earliest')
    kafka_consumer.subscribe(etl_config.kafka_topic)
    ch_client = Client(host=etl_config.clickhouse)
    return kafka_consumer, ch_client


def load(kafka_consumer, ch_client):
    while True:
        logging.info('starting etl')
        events = kafka_extractor.extract_data(kafka_consumer)
        ch_table, transformed_data = transform(events, etl_config.kafka_topic)
        clickhouse_loader.load_data(ch_client, transformed_data, ch_table)
        time.sleep(etl_config.repeat_time_in_seconds)


if __name__ == '__main__':
    kafka_consumer, ch_client = connect()
    load(kafka_consumer, ch_client)
