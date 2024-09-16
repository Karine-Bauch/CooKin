import requests

weather_api = "https://wttr.in/"

def get_weather(location: str):
    weather_url = f"{weather_api}{location}?format=j1"
    return requests.get(weather_url).json()


if __name__ == '__main__':
    print(get_weather("lauris"))