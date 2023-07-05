import logging
from http import HTTPStatus

import uvicorn
from aiokafka import AIOKafkaProducer
from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import ORJSONResponse
from httpx import RequestError

from api.v1 import ugc
from core.logger import LOGGING
from db import kafka
from core.config import app_config, kafka_config

from dotenv import load_dotenv

load_dotenv()


app = FastAPI(
    title=app_config.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    kafka.kafka = AIOKafkaProducer(bootstrap_servers=f'{kafka_config.broker_host}:{kafka_config.broker_port}')
    await kafka.kafka.start()


@app.on_event('shutdown')
async def shutdown():
    await kafka.kafka.stop()


app.include_router(ugc.router, prefix='/api/v1/ugc', tags=['ugc'])


@app.exception_handler(RequestError)
async def bad_storage_request_exception_handler(request, exc):
    http_exc = HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=exc.error)
    return await http_exception_handler(request, http_exc)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=app_config.host,
        port=app_config.port,
        log_config=LOGGING,
        log_level=logging.DEBUG if app_config.is_debug else logging.INFO,
    )
