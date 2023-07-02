from fastapi import APIRouter, Depends, Header

from api.v1.auth.auth_bearer import BaseJWTBearer
from api.v1.models.ugc import EventWatchResp, EventWatch
from core.config import kafka_config
from services.ugc import EventService, get_event_service

router = APIRouter()


@router.post(
    '/event_watch',
    response_model=EventWatchResp,
    description='Отправка события о просмотре фильма в Kafka',
    dependencies=[Depends(BaseJWTBearer())]
)
async def event_handler(
        body: EventWatch,
        authorization: str = Header(None),
        event_service: EventService = Depends(get_event_service)
):
    """
    Отправляем временную метку unix timestamp, соответствующую текущему месту просмотра фильма пользователем
    """
    # Todo нужно реализовать получение user_uuid из токена
    bearer_token = authorization.split(" ")[1]

    # Todo нужно реализовать отправку события в Kafka https://dpaste.org/mrg5U#L3,4
    await event_service.send_event(
        topic=kafka_config.kafka_topic,
        value=bytearray(str(body.watch_time), 'utf-8'),
        key=bytearray(bearer_token + "+" + str(body.film_id), 'utf-8'),
    )

    return EventWatchResp(
        msg='Event watch time successfully sent',
        user_uuid=bearer_token,  # Todo нужно заменить на user_uuid
        film_id=body.film_id,
        watch_time=body.watch_time
    )
