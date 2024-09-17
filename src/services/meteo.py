import httpx

weather_api = "https://wttr.in/test/"


def get_weather(location: str) -> dict:
    weather_url = f"{weather_api}{location}?format=j1" # font case managed by wttr API

    try:
        weather = httpx.get(weather_url)
        weather.raise_for_status()
        return weather.json()
    except httpx.HTTPStatusError as e:
        raise e


if __name__ == "__main__":
    print(get_weather("Bordeaux"))
