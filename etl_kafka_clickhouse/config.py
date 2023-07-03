from pydantic import BaseSettings, Field


class Config(BaseSettings):
   kafka: str = Field(env='KAFKA_HOST')
   clickhouse: str = Field('localhost:9092', env='CLICKHOUSE_HOST')
   repeat_time_in_seconds: int = Field(env='ETL_REPEAT_TIME')

