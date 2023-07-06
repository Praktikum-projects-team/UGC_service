import logging
from dataclasses import astuple

from clickhouse_driver import Client
from typing import Optional

ch_client: Optional[Client] = None


def load_data(transformed_events, table_name: str):
    data = []
    table_fields = ', '.join(list(transformed_events[0].__annotations__.keys()))
    for event in transformed_events:
        data.append(str(astuple(event)))
    ch_client.execute(
        """INSERT INTO default.{table}
           ({fields})
           VALUES {values}""".format(table=table_name, fields=table_fields, values=', '.join(data)))
