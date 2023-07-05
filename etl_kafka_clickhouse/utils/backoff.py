from functools import wraps
import time


def backoff(exceptions: tuple, start_sleep_time=0.1, factor=2, border_sleep_time=10):
    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            t = start_sleep_time
            while True:
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    t = t * factor
                    if t > border_sleep_time:
                        t = border_sleep_time
                    time.sleep(t)

        return inner

    return func_wrapper
