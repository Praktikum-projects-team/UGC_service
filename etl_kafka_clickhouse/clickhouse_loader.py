from dataclasses import astuple


def load_data(ch_client, transformed_events, table_name: str):
    data = []
    table_fields = ', '.join(list(transformed_events[0].__annotations__.keys()))
    for event in transformed_events:
        data.append(astuple(event))
    ch_client.execute(
        """INSERT INTO default.{table}
           ({fields})
           VALUES""".format(table=table_name, fields=table_fields), data)
