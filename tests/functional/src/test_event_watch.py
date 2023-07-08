from http import HTTPStatus

import pytest

from tests.functional.testdata.watch_event import get_watch_data
from tests.functional.utils.routes import EVENT_WATCH_URL

pytestmark = pytest.mark.asyncio


class TestEventWatch:

    async def test_event_watch(self, make_post_request, user_access_token):
        watch_data = await get_watch_data()
        resp = await make_post_request(EVENT_WATCH_URL, data=watch_data[0], token=user_access_token)

        assert resp.status == HTTPStatus.OK, 'Wrong status code'
        assert resp.body['msg'] == 'Event watch time successfully sent', 'Wrong message'

    @pytest.mark.parametrize('token', [None, 'invalid_token'])
    async def test_event_watch_invalid_token(self, make_post_request, token):
        watch_data = await get_watch_data()
        resp = await make_post_request(EVENT_WATCH_URL, data=watch_data[0], token=token)

        assert resp.status == HTTPStatus.FORBIDDEN, 'Wrong status code'
        assert resp.body['detail'] == 'Invalid token or expired token.', 'Wrong message'

    async def test_event_watch_without_token(self, make_post_request):
        watch_data = await get_watch_data()
        resp = await make_post_request(EVENT_WATCH_URL, data=watch_data[0], token='')

        assert resp.status == HTTPStatus.FORBIDDEN, 'Wrong status code'
        assert resp.body['detail'] == 'Not authenticated', 'Wrong message'

    @pytest.mark.parametrize('watch_time', ['12345', 12345, 1, 0])
    async def test_event_watch_time(self, make_post_request, user_access_token, watch_time):
        watch_data = await get_watch_data()
        watch_data[0]['watch_time'] = watch_time
        resp = await make_post_request(EVENT_WATCH_URL, data=watch_data[0], token=user_access_token)

        assert resp.status == HTTPStatus.OK, 'Wrong status code'
        assert resp.body['msg'] == 'Event watch time successfully sent', 'Wrong message'

    @pytest.mark.parametrize('watch_time', ['', '123qwe', '***', [1, 2, 3]])
    async def test_event_watch_time_invalid(self, make_post_request, user_access_token, watch_time):
        watch_data = await get_watch_data()
        watch_data[0]['watch_time'] = watch_time
        resp = await make_post_request(EVENT_WATCH_URL, data=watch_data[0], token=user_access_token)

        assert resp.status == HTTPStatus.UNPROCESSABLE_ENTITY, 'Wrong status code'
        assert resp.body['detail'][0]['loc'] == ["body", "watch_time"], 'Wrong location'
        assert resp.body['detail'][0]['msg'] == 'value is not a valid integer', 'Wrong message'
        assert resp.body['detail'][0]['type'] == 'type_error.integer', 'Wrong type'

    @pytest.mark.parametrize('film_id', [1, 0, -1, 100, '123', '', '123qwe', '***', [1, 2, 3]])
    async def test_event_film_id_invalid(self, make_post_request, user_access_token, film_id):
        watch_data = await get_watch_data()
        watch_data[0]['film_id'] = film_id
        resp = await make_post_request(EVENT_WATCH_URL, data=watch_data[0], token=user_access_token)

        assert resp.status == HTTPStatus.UNPROCESSABLE_ENTITY, 'Wrong status code'
        assert resp.body['detail'][0]['loc'] == ["body", "film_id"], 'Wrong location'
        assert resp.body['detail'][0]['msg'] == 'value is not a valid uuid', 'Wrong message'
        assert resp.body['detail'][0]['type'] == 'type_error.uuid', 'Wrong type'
