from abc import ABC, abstractmethod
from aiokafka import AIOKafkaProducer


class AbstractEventProducer(ABC):
    """Абстрактный класс для подключения к хранилищу"""

    def __init__(self, broker: AIOKafkaProducer):
        """
        Конструктор класса AbstractEventProducer
        :param broker: экземпляр AIOKafkaProducer
        """
        self.broker = broker

    @abstractmethod
    def send(self, topic: str, value: bytes, key: bytes):
        """Метод отправки данных в хранилище"""
        raise NotImplementedError


class KafkaProducer(AbstractEventProducer):
    """
    Класс для отправки данных в Kafka
    """

    async def send(self, topic: str, value: bytes, key: bytes):
        """
        Метод отправки данных в Kafka
        :param topic: топик в Kafka
        :param value: тело сообщения
        :param key: ключ сообщения
        """
        await self.broker.send(topic=topic, value=value, key=key)
