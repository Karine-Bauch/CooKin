import httpx

from services import utils

weather_api = "https://wttr.in/"


def check_city(city):
    open_streetmap_url = (
        f"https://nominatim.openstreetmap.org/search?city={city}&format=json"
    )
    response = httpx.get(open_streetmap_url).json()
    if response:
        return True
    return False


def weather_api_call(location):
    if check_city(location):
        weather_url = f"{weather_api}{location}?format=j1"
    else:
        raise KeyError(f'Location "{location}" not found.')
    return httpx.get(weather_url).json()


def get_weather(location) -> dict:
    try:
        weather = utils.retry(weather_api_call, lambda response: response, location)
    except TimeoutError as e:
        raise TimeoutError from e
    return weather


if __name__ == "__main__":
    print(check_city("London"))
    print(get_weather("London"))
    print(check_city("58913784137849318840134134"))
    print(get_weather("58913784137849318840134134"))
