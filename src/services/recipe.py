import os

import dotenv
import openai
import openai.types.chat

import services.exc
import services.utils
import services.weather

dotenv.load_dotenv()


openai_key = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI(api_key=openai_key)


def create_prompt(humidity, temperature, weather_description, wind_speed) -> str:
    prompt = (
        f"The weather is {weather_description}, max temperature of the day is {temperature} celsius degrees, "
        f"with a wind at {wind_speed} kmph and {humidity}% of humidity. "
        f"Give me a recipe adapted to the weather."
    )
    return prompt


def openai_api_call(prompt) -> openai.types.chat.ChatCompletion:
    return client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=1,
        messages=[
            {
                "role": "system",
                "content": "You're Yoda. You must explain like him for all your answer."
                "For the entire answer you must explain like Yoda. Write in French",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

@services.utils.retry(lambda response: response)
def get_recipe(city: str) -> str | None:
    weather: dict = services.weather.get_weather(city)

    weather_description: str = weather["current_condition"][0]["weatherDesc"][0][
        "value"
    ]
    temperature: str = weather["current_condition"][0]["temp_C"]
    humidity: str = weather["current_condition"][0]["humidity"]
    wind_speed: str = weather["current_condition"][0]["windspeedKmph"]

    openai_prompt: str = create_prompt(
        humidity, temperature, weather_description, wind_speed
    )

    completion: openai.types.chat.ChatCompletion = openai_api_call(openai_prompt)

    return completion.choices[0].message.content


if __name__ == "__main__":
    print(create_prompt(80, 25, "partially cloudy", 12))
    print(get_recipe("Marseille"))
