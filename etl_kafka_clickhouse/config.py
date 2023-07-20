from pydantic import BaseSettings, Field
from dotenv import load_dotenv

load_dotenv()


class Config(BaseSettings):
    kafka: str = Field(env='KAFKA_HOST')
    clickhouse: str = Field(env='CLICKHOUSE_HOST')
    repeat_time_in_seconds: int = Field(env='ETL_REPEAT_TIME')
    kafka_topic: str = Field('views', env='KAFKA_TOPIC')
    kafka_group_id: str = Field('echo-messages-to-stdout', env='KAFKA_GROUP_ID')
    kafka_data_size: int = Field(100, env='KAFKA_DATA_SIZE')


etl_config = Config()  # type: ignore[call-arg]
