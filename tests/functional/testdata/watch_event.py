import uuid
from datetime import datetime


async def get_watch_data(n: int = 1) -> list[dict]:
    return [{
        'film_id': str(uuid.uuid4()),
        'watch_time': 1234
    } for _ in range(n)]
