from fastapi import Depends
from aiokafka import AIOKafkaProducer

from db.kafka import get_kafka
from utils.kafka_producer import AbstractProducer, KafkaProducer


class EventService:
    """
    Сервис взаимодействия с Kafka
    """
    def __init__(self, kafka: AbstractProducer):
        self.kafka = kafka

    async def send_event(self, topic: str, value: bytes, key: bytes):
        """
        Метод отправки события в Kafka
        :param topic: топик в Kafka
        :param value: тело сообщения
        :param key: ключ сообщения
        """
        await self.kafka.send(topic=topic, value=value, key=key)


def get_event_service(
        kafka: AIOKafkaProducer = Depends(get_kafka)
) -> EventService:
    """
    Провайдер EventService, с помощью Depends он сообщает, что ему необходим AIOKafkaProducer
    """
    return EventService(KafkaProducer(kafka))
