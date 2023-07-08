from tests.functional.settings import test_settings

BASE_URL = '/api/v1'

# AUTH_URL = f'http:/{BASE_URL}/auth'
UGC_URL = f'{BASE_URL}/ugc'

EVENT_WATCH_URL = f'{UGC_URL}/event_watch'
AUTH_URL_SIGN_UP = f'{test_settings.auth_host}/sign_up'
AUTH_URL_LOGIN = f'{test_settings.auth_host}/login'
