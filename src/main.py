import logging
from contextlib import asynccontextmanager
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


@asynccontextmanager
async def lifespan(application: FastAPI):
    kafka.kafka = AIOKafkaProducer(bootstrap_servers=kafka_config.kafka_server)
    await kafka.kafka.start()
    yield
    await kafka.kafka.stop()


app = FastAPI(
    title=app_config.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)


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
