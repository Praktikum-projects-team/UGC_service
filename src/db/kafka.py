from typing import Optional
from aiokafka import AIOKafkaProducer
from fastapi import Depends

from utils.kafka_producer import KafkaProducer

kafka: Optional[AIOKafkaProducer] = None


# Для внедрения зависимостей
async def get_kafka() -> AIOKafkaProducer:
    return kafka


def get_event_producer(
        kafka: AIOKafkaProducer = Depends(get_kafka)
) -> KafkaProducer:
    """
    Функция для получения экземпляра KafkaProducer
    """
    return KafkaProducer(kafka)
