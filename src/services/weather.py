import httpx

import services.utils
from services.exc import NotFound

weather_api = "https://wttr.in/"


def check_city(city) -> None:
    open_streetmap_url = (
        f"https://nominatim.openstreetmap.org/search?city={city}&format=json"
    )
    response = httpx.get(open_streetmap_url)
    response.raise_for_status()
    if not response.json():
        raise NotFound


def weather_api_call(location) -> dict:
    check_city(location)
    weather_url = f"{weather_api}{location}?format=j1"
    weather = httpx.get(weather_url)
    return weather.json()


@services.utils.retry(lambda response: response)
def get_weather(location) -> dict:
    return weather_api_call(location)

if __name__ == "__main__":
    # print(check_city("London"))
    # print(get_weather("London"))
    print(get_weather_deco('London'))
    # print(check_city("58913784137849318840134134"))
    # print(get_weather("58913784137849318840134134"))
