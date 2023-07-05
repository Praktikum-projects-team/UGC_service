from dataclasses import dataclass, field
from datetime import datetime

from dacite import from_dict

# import timestamp


@dataclass
class MovieViews:
    movie_id: str
    user_id: str
    view_progress: str
    created_at: str
    # table_name: str = field(default='movie_views')


@dataclass
class Views:
    film_id: str
    user_id: str
    watch_time: str
    created_at: str

    def transform_to_ch(self):
        created_at = datetime.fromisoformat(self.created_at).strftime("%Y-%m-%d %H:%M:%S")
        return MovieViews(movie_id=self.film_id, user_id=self.user_id,
                          view_progress=self.watch_time, created_at=created_at)


topics_tables = {'views': Views}


def transform(events: list, topic: str):
    return [event.transform_to_ch() for event in [from_dict(data_class=topics_tables[topic], data=i) for i in events]]
