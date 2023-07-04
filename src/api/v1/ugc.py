import json
from datetime import datetime

from fastapi import APIRouter, Depends, Request

from api.v1.auth.auth_bearer import BaseJWTBearer
from api.v1.models.ugc import EventWatchResp, EventWatch
from core.config import kafka_config
from services.auth_api import AuthApi
from services.ugc import EventService, get_event_service

router = APIRouter()
auth_api = AuthApi()


@router.post(
    '/event_watch',
    response_model=EventWatchResp,
    description='Отправка события о просмотре фильма в Kafka',
    dependencies=[Depends(BaseJWTBearer())]
)
async def event_handler(
        body: EventWatch,
        request: Request,
        event_service: EventService = Depends(get_event_service)
):
    """
    Отправляем временную метку unix timestamp, соответствующую текущему месту просмотра фильма пользователем
    """
    current_user = request.token_payload  # type: ignore

    data_event = {
        "user_id": str(current_user["id"]),
        "film_id": str(body.film_id),
        "watch_time": str(body.watch_time),
        "created_at": str(datetime.utcnow())
    }

    # Todo нужно реализовать отправку события в Kafka https://dpaste.org/mrg5U#L3,4
    await event_service.send_event(
        topic=kafka_config.kafka_topic,
        value=bytearray(json.dumps(data_event), 'utf-8'),
        key=bytearray(current_user["id"] + "+" + str(body.film_id), 'utf-8'),
    )

    return EventWatchResp(msg='Event watch time successfully sent')
