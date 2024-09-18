import time
import typing

import httpx

weather_api = "https://wttr.in/"


def check_city(city):
    open_streetmap_url = (
        f"https://nominatim.openstreetmap.org/search?city={city}&format=json"
    )
    response = httpx.get(open_streetmap_url).json()
    if response:
        return True
    return False


INCREMENTAL_WAIT = [1, 3, 5, 8, 13]

def retry(api_call: typing.Callable, predicate: typing.Callable, *args, **kwargs):
    for wait in INCREMENTAL_WAIT:
        weather = api_call(*args, **kwargs)
        if predicate(weather):
            return weather
        print(f"Retry, waiting {wait} seconds")
        time.sleep(wait)
    raise TimeoutError


def weather_api_call(location):
    if check_city(location):
        weather_url = f"{weather_api}{location}?format=j1"
    else:
        raise KeyError(f'Location "{location}" not found.')
    return httpx.get(weather_url)

def get_weather(location) -> dict:
    try:
        weather = retry(weather_api_call, lambda response: response, location)
    except TimeoutError as e:
        raise TimeoutError from e

    return weather.json()


if __name__ == "__main__":
    print(check_city("London"))
    print(get_weather("London"))
    print(check_city("58913784137849318840134134"))
    print(get_weather("58913784137849318840134134"))
