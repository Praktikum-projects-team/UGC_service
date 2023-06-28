import math
import random
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta
from uuid import UUID, uuid4

from more_itertools import chunked


@dataclass
class ViewHistory:
    created_at: datetime = datetime.min
    user_id: UUID = uuid4()
    film_id: UUID = uuid4()
    timestamp: int = 0

    def to_dict(self):
        return {
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'user_id': str(self.user_id),
            'film_id': str(self.film_id),
            'timestamp': self.timestamp,
        }


class ViewHistoryCollection(list[ViewHistory]):
    def __init__(self, total: int, user_count: int, film_count: int):
        super().__init__(ViewHistory() for _ in range(total))
        self._set_users(user_count)
        self._set_film(film_count)
        self._set_timestamps()

    def to_dict(self):
        return [view.to_dict() for view in self]

    @property
    def _map_by_user_film(self):
        dict_: dict[str, list[ViewHistory]] = defaultdict(list)
        for view in self:
            dict_[str(view.user_id) + str(view.film_id)].append(view)
        return dict_

    def _set_users(self, user_count: int):
        user_ids = [uuid4() for _ in range(user_count)]
        chunk_count = math.ceil(len(self) / user_count)
        for user_id_idx, user_chunk in enumerate(chunked(self, chunk_count)):
            for user in user_chunk:
                user.user_id = user_ids[user_id_idx]

    def _set_film(self, film_count: int):
        film_ids = [uuid4() for _ in range(film_count)]
        chunk_count = math.ceil(len(self) / film_count)
        for film_id_idx, film_chunk in enumerate(chunked(self, chunk_count)):
            for film in film_chunk:
                film.film_id = film_ids[film_id_idx]

    def _set_timestamps(self):
        for views in self._map_by_user_film.values():
            start_datetime = datetime(2020, 1, 1, 0, 0, 0)
            for view in views:
                view.created_at = start_datetime
                view.timestamp += random.randint(1, 5)
                start_datetime += timedelta(seconds=5)
