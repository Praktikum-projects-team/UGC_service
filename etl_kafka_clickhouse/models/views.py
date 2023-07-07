from dataclasses import dataclass
from datetime import datetime


@dataclass
class MovieViews:
    movie_id: str
    user_id: str
    view_progress: int
    created_at: datetime


@dataclass
class Views:
    film_id: str
    user_id: str
    watch_time: str
    created_at: str

    def transform_to_ch(self):
        created_at = datetime.fromisoformat(self.created_at)
        return MovieViews(movie_id=self.film_id, user_id=self.user_id,
                          view_progress=int(self.watch_time), created_at=created_at)


TOPICS_TABLES = {'views': (Views, 'movie_views')}
