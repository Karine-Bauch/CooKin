import os

import dotenv
import httpx
import openai

import services.exc
import services.weather

dotenv.load_dotenv()


openai_key = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI(api_key=openai_key)


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

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.5,
        messages=[
            {
                "role": "system",
                "content": f"You're from {city} region, deeply connected to the local traditions and culture. "
                f"Explain you in the {country} language with many local expressions. "
                f"The weather is {weather_description}, max temperature of the day {temperature} celsius degrees, "
                f"with a wind at {wind_speed} kmph and {humidity}% of humidity.",
            },
            {
                "role": "user",
                "content": " Give me an original recipe perfect for the weather.",
            },
        ],
    )

    return completion.choices[0].message.content


if __name__ == "__main__":
    print(get_recipe("Marseille"))
