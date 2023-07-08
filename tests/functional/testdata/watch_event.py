import uuid
from datetime import datetime


async def get_watch_data(n: int = 1) -> list[dict]:
    return [{
        'film_id': str(uuid.uuid4()),
        'watch_time': datetime.utcnow()
    } for _ in range(n)]
