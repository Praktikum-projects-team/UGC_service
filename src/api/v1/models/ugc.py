from uuid import UUID

from core.base_model import OrjsonBaseModel


class EventWatch(OrjsonBaseModel):
    film_id: UUID
    watch_time: int


class EventWatchResp(OrjsonBaseModel):
    msg: str
