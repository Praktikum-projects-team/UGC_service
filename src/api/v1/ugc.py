from fastapi import APIRouter, Depends, Request

from api.v1.auth.auth_bearer import BaseJWTBearer
from api.v1.models.ugc import EventWatch, EventWatchResp
from services.auth import AuthApi
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
) -> EventWatchResp:
    """
    Отправляем временную метку unix timestamp, соответствующую текущему месту просмотра фильма пользователем
    """
    current_user = request.token_payload  # type: ignore
    await event_service.send_event(current_user, body)

    return EventWatchResp(msg='Event watch time successfully sent')
