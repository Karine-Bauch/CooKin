import os

import openai
import dotenv

dotenv.load_dotenv()


openai_key = os.getenv('OPENAI_API_KEY')
print(openai_key)

client = openai.OpenAI(api_key=openai_key)

def get_recipe(location: str, weather: str, temperature: float, humidity: float):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"You're from {location} region, deeply connected to the local traditions and culture. "
                           f"You speak with local expressions. Explain you in the country language of {location}. "
                           f"The weather is {weather}, max temperature of the day {temperature} celsius degrees and "
                           f"{humidity}% of humidity."
            },
            {
                "role": "user",
                "content": " Give me an original recipe perfect for the weather."
            },
        ]
    )
    return completion


if __name__ == "__main__":
    print(get_recipe("Bordeaux", "cloudy", 20, 99).choices[0].message.content)