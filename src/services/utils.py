import contextlib
import time
import typing
import functools

import httpx
import openai.types.chat

INCREMENTAL_WAIT = [1, 3, 5, 8, 13]


def retry(predicate: typing.Callable):
    def decorator(fct: typing.Callable):
        @functools.wraps(fct)
        def wrapper(*args, **kwargs):
            for wait in INCREMENTAL_WAIT:
                with contextlib.suppress(httpx.TimeoutException):
                    result = fct(*args, **kwargs)
                    if predicate(result):
                        return result
                print(f"Retry, waiting {wait} seconds")
                time.sleep(wait)
            raise TimeoutError
        return wrapper
    return decorator
