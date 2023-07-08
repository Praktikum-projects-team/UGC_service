from http import HTTPStatus

import pytest

from tests.functional.testdata.watch_event import get_watch_data
from tests.functional.utils.routes import EVENT_WATCH_URL


pytestmark = pytest.mark.asyncio


class EventWatch:
    async def test_evetn_watch_example(self, make_post_request):
        watch_data = await get_watch_data()
        response = await make_post_request(EVENT_WATCH_URL, watch_data[0])

        assert response.status == HTTPStatus.OK, 'Wrong status code'
