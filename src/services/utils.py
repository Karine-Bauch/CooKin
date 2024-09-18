import time
import typing

INCREMENTAL_WAIT = [1, 3, 5, 8, 13]


def retry(api_call: typing.Callable, predicate: typing.Callable, *args, **kwargs):
    for wait in INCREMENTAL_WAIT:
        weather = api_call(*args, **kwargs)
        if predicate(weather):
            return weather
        print(f"Retry, waiting {wait} seconds")
        time.sleep(wait)
    raise TimeoutError
