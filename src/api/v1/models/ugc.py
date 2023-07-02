from core.base_model import OrjsonBaseModel


class EventWatch(OrjsonBaseModel):
    film_id: int
    watch_time: int


class EventWatchResp(OrjsonBaseModel):
    msg: str
    user_uuid: str
    film_id: int
    watch_time: int
