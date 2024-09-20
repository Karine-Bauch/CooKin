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
    return httpx.get(weather_url).json()


def get_weather(location) -> dict:
    return services.utils.retry(
            weather_api_call, lambda response: response, location
        )


if __name__ == "__main__":
    print(check_city("London"))
    print(get_weather("London"))
    print(check_city("58913784137849318840134134"))
    print(get_weather("58913784137849318840134134"))
