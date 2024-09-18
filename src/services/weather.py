import httpx

weather_api = "https://wttr.in/"

def check_city(city):
    open_streetmap_url = f"https://nominatim.openstreetmap.org/search?city={city}&format=json"
    response = httpx.get(open_streetmap_url).json()
    if response:
        return True
    return False

def get_weather(location: str) -> dict:
    if check_city(location):
        weather_url = f"{weather_api}{location}?format=j1"
    else:
        raise KeyError(f'Location "{location}" not found.')

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
