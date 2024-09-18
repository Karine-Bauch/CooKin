import os

import dotenv
import httpx
import openai

import services.exc
import services.weather
from services import utils

dotenv.load_dotenv()


openai_key = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI(api_key=openai_key)


def create_prompt(
    city, country, humidity, temperature, weather_description, wind_speed
) -> str:
    prompt = (
        f"You're from {city}, deeply connected to the local traditions and culture. "
        f"Explain you in the {country} language with many local expressions of {city}. "
        f"The weather is {weather_description}, max temperature of the day is {temperature} celsius degrees, "
        f"with a wind at {wind_speed} kmph and {humidity}% of humidity."
    )
    return prompt


def openai_api_call(prompt):
    return client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=1,
        messages=[
            {
                "role": "system",
                "content": prompt,
            },
            {
                "role": "user",
                "content": " Give me an original recipe perfect for the weather.",
            },
        ],
    )


def get_recipe(city: str) -> str:
    try:
        weather: dict = services.weather.get_weather(city)
        country: str = weather["nearest_area"][0]["country"][0]["value"]
        weather_description: str = weather["current_condition"][0]["weatherDesc"][0][
            "value"
        ]
        temperature: str = weather["current_condition"][0]["temp_C"]
        humidity: str = weather["current_condition"][0]["humidity"]
        wind_speed: str = weather["current_condition"][0]["windspeedKmph"]

    except httpx.HTTPError as e:
        raise services.exc.RecipeNotFound(
            f"Recipe not Found for this location: {city}. " f"{e}"
        )

    openai_prompt: str = create_prompt(
        city, country, humidity, temperature, weather_description, wind_speed
    )
    try:
        completion = utils.retry(
            openai_api_call, lambda response: response, openai_prompt
        )
    except TimeoutError as e:
        raise TimeoutError from e

    return completion.choices[0].message.content


if __name__ == "__main__":
    print(create_prompt("Paris", "France", 80, 25, "partially cloudy", 12))
    print(get_recipe("Marseille"))
