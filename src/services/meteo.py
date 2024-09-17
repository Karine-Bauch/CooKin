import httpx

weather_api = "https://wttr.in/"


def get_weather(location: str) -> dict:
    weather_url = f"{weather_api}{location}?format=j1"
    return httpx.get(weather_url).json()


if __name__ == "__main__":
    print(get_weather("lauris"))
