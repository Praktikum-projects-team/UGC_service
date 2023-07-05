from dataclasses import astuple

from clickhouse_driver import Client
from typing import Optional

ch_client: Optional[Client] = None


def load_data(transformed_events, table_name: str):
    data = []
    for event in transformed_events:
        data.append(str(astuple(event)))
    ch_client.execute(
        f'''INSERT INTO default.{table_name}
        ({', '.join(list(transformed_events[0].__annotations__.keys()))})
        VALUES {', '.join(data)}''')


def check():
    print(ch_client.execute('select * from default.movie_views'))

