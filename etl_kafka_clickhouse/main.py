import logging

from kafka import KafkaConsumer, errors as kafka_errors
from clickhouse_driver import Client, errors as ch_errors
import time
from config import etl_config
import kafka_extractor
from transformer import transform
import clickhouse_loader
from utils.backoff import backoff

logging.basicConfig(level=logging.INFO)


@backoff(exceptions=(kafka_errors.NoBrokersAvailable, ch_errors.NetworkError))
def connect():
    kafka_extractor.consumer = KafkaConsumer(etl_config.kafka_topic,
                                             bootstrap_servers=[etl_config.kafka],
                                             group_id=etl_config.kafka_group_id,
                                             auto_offset_reset='earliest')
    kafka_extractor.consumer.subscribe(etl_config.kafka_topic)
    clickhouse_loader.ch_client = Client(host=etl_config.clickhouse)


def load():
    while True:
        logging.info('starting etl')
        events = kafka_extractor.extract_data()
        ch_table, transformed_data = transform(events, etl_config.kafka_topic)
        clickhouse_loader.load_data(transformed_data, ch_table)
        time.sleep(etl_config.repeat_time_in_seconds)


if __name__ == '__main__':
    connect()
    load()
