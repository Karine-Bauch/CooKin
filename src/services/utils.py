import contextlib
import time
import typing

import httpx

INCREMENTAL_WAIT = [1, 3, 5, 8, 13]


def retry(api_call: typing.Callable, predicate: typing.Callable, *args, **kwargs):
    for wait in INCREMENTAL_WAIT:
        with contextlib.suppress(httpx.TimeoutException):
            result = api_call(*args, **kwargs)
            if predicate(result):
                return result
        print(f"Retry, waiting {wait} seconds")
        time.sleep(wait)
    raise TimeoutError
