import json
from datetime import datetime

from fastapi import Depends

from api.v1.models.ugc import EventWatch
from core.config import kafka_config
from utils.kafka_producer import AbstractEventProducer, KafkaProducer, get_event_producer


class EventService:
    """
    Сервис взаимодействия с Kafka
    """
    def __init__(self, kafka: AbstractEventProducer):
        self.kafka = kafka

    async def send_event(self, current_user: dict, event_info: EventWatch):
        """
        Метод отправки события в Kafka
        :param current_user: информация о пользователе
        :param event_info: информация о событии
        """

        event_data = {
            "user_id": str(current_user["id"]),
            "film_id": str(event_info.film_id),
            "watch_time": str(event_info.watch_time),
            "created_at": str(datetime.utcnow())
        }

        topic = kafka_config.kafka_topic
        value = bytearray(json.dumps(event_data), 'utf-8')
        key = bytearray(current_user["id"] + "+" + str(event_data["film_id"]), 'utf-8')

        await self.kafka.send(topic=topic, value=value, key=key)


def get_event_service(
        producer: KafkaProducer = Depends(get_event_producer)
) -> EventService:
    """
    Провайдер EventService, с помощью Depends он сообщает, что ему необходим AIOKafkaProducer
    """
    return EventService(producer)
