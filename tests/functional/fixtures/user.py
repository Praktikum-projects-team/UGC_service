import logging
from http import HTTPStatus

import pytest
import requests

from tests.functional.utils.constants import UserData
from tests.functional.utils.routes import AUTH_URL_LOGIN, AUTH_URL_SIGN_UP


@pytest.fixture(scope="session", autouse=True)
async def create_user_default():
    requests.post(AUTH_URL_SIGN_UP, json={
        'login': UserData.LOGIN,
        'password': UserData.PASSWORD,
        'name': UserData.NAME
    })
    logging.info("User successfully created")


@pytest.fixture(scope="session")
async def user_access_token():
    resp = requests.post(AUTH_URL_LOGIN, json={
        'login': UserData.LOGIN,
        'password': UserData.PASSWORD
    })
    resp_data = resp.json()
    if resp.status_code != HTTPStatus.OK:
        raise Exception(resp_data['message'])

    return resp_data['access_token']
