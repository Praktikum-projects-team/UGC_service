import os

from pydantic import BaseSettings, Field

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class AppConfig(BaseSettings):
    base_dir: str = BASE_DIR
    project_name: str = Field(..., env='PROJECT_NAME')
    host: str = Field(..., env='APP_HOST')
    port: int = Field(..., env='APP_PORT')
    is_debug: bool = Field(..., env='IS_DEBUG')


class AuthConfig(BaseSettings):
    host: str = Field(..., env='AUTH_HOST')
    jwt_secret: str = Field(..., env='JWT_SECRET')
    jwt_algorithm: str = Field(..., env='JWT_ALGORITHM')


class KafkaConfig(BaseSettings):
    # host: str = Field(..., env='KAFKA_HOST')
    # port: int = Field(..., env='KAFKA_PORT')

    kafka_server: str = Field('localhost:9092', env='KAFKA_HOST')
    kafka_topic: str = Field('views', env='KAFKA_TOPIC')


app_config = AppConfig()
auth_config = AuthConfig()
kafka_config = KafkaConfig()
