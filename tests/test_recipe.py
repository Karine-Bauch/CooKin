import pytest

import services.recipe
import services.weather


def test_check_city() -> None:
    assert services.weather.check_city('London') == True
    assert services.weather.check_city('Aix en Provence') == True
    assert services.weather.check_city('this is not a city') == False


def test_weather_return_dict() -> None:
    weather = services.weather.get_weather("London")
    assert isinstance(weather, dict)


def test_weather_has_fields() -> None:
    weather = services.weather.get_weather("London")
    assert weather["nearest_area"][0]["country"][0]["value"]
    assert weather["current_condition"][0]["weatherDesc"][0]["value"]
    assert weather["current_condition"][0]["temp_C"]
    assert weather["current_condition"][0]["humidity"]
    assert weather["current_condition"][0]["windspeedKmph"]


@pytest.mark.usefixtures("mock_get_weather")
def test_prompt() -> None:
    weather = services.weather.get_weather("London")
    prompt = services.recipe.create_prompt(
        "London",
            weather["nearest_area"][0]["country"][0]["value"],
            weather["current_condition"][0]["weatherDesc"][0]["value"],
            weather["current_condition"][0]["temp_C"],
            weather["current_condition"][0]["humidity"],
            weather["current_condition"][0]["windspeedKmph"],
    )
    assert len(prompt) > 0
    assert weather["nearest_area"][0]["country"][0]["value"] in prompt
    assert weather["current_condition"][0]["weatherDesc"][0]["value"] in prompt
    assert weather["current_condition"][0]["temp_C"] in prompt
    assert weather["current_condition"][0]["humidity"] in prompt
    assert weather["current_condition"][0]["windspeedKmph"] in prompt


@pytest.mark.usefixtures("mock_get_weather")
def test_recipe() -> None:
    recipe = services.recipe.get_recipe("Paris")
    assert isinstance(recipe, str)
    assert len(recipe) > 0