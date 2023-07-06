from models.views import TOPICS_TABLES


def transform(events: list, topic: str):
    model, table = TOPICS_TABLES[topic]
    return table, [event.transform_to_ch() for event in [model(**i) for i in events]]
