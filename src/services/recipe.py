import os

import openai
import dotenv

import services.meteo

dotenv.load_dotenv()


openai_key = os.getenv("OPENAI_API_KEY")
print(openai_key)

client = openai.OpenAI(api_key=openai_key)


def get_recipe(city: str) -> str:
    weather: dict = services.meteo.get_weather(city)
    weather_description: str = weather["current_condition"][0]["weatherDesc"][0][
        "value"
    ]
    temperature: str = weather["current_condition"][0]["temp_C"]
    humidity: str = weather["current_condition"][0]["humidity"]
    wind_speed: str = weather["current_condition"][0]["windspeedKmph"]

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"You're from {city} region, deeply connected to the local traditions and culture. "
                f"You speak with local expressions. Explain you in the country language of {city}. "
                f"The weather is {weather_description}, max temperature of the day {temperature} celsius degrees, "
                f"with a wind at {wind_speed} kmph and {humidity}% of humidity.",
            },
            {
                "role": "user",
                "content": " Give me an original recipe perfect for the weather.",
            },
        ],
    )
    print(completion)
    return completion.choices[0].message.content


if __name__ == "__main__":
    print(get_recipe("Bordeaux"))
