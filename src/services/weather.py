import httpx

weather_api = "https://wttr.in/"


def get_weather(location: str) -> dict:
    weather_url = f"{weather_api}{location}?format=j1"  # font case managed by wttr API

    try:
        weather = httpx.get(weather_url)
    except TimeoutError as e:
        raise TimeoutError from e

    return weather.json()



if __name__ == "__main__":
    print(check_city("London"))
    print(get_weather("London"))
    print(check_city("58913784137849318840134134"))
    print(get_weather("58913784137849318840134134"))
