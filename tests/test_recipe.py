import pytest

import services.recipe
import services.weather


def test_check_city() -> None:
    assert services.weather.check_city("London")
    assert services.weather.check_city("Aix en Provence")
    assert not services.weather.check_city("this is not a city")


def test_get_weather_dict() -> None:
    weather = services.weather.get_weather("London")
    assert isinstance(weather, dict)


def test_weather_has_needed_fields() -> None:
    weather = services.weather.get_weather("London")
    assert weather["nearest_area"][0]["country"][0]["value"]
    assert weather["current_condition"][0]["weatherDesc"][0]["value"]
    assert weather["current_condition"][0]["temp_C"]
    assert weather["current_condition"][0]["humidity"]
    assert weather["current_condition"][0]["windspeedKmph"]


@pytest.mark.usefixtures("mock_get_weather")
def test_prompt_creation() -> None:
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
def test_get_recipe_from_ai() -> None:
    recipe = services.recipe.get_recipe("Paris")
    assert isinstance(recipe, str)
    assert len(recipe) > 0


@pytest.mark.usefixtures("mock_weather_api_call")
def test_retry_weather_api_call():
    weather = services.weather.get_weather("London")
    assert isinstance(weather, dict)


@pytest.mark.usefixtures("mock_weather_api_call_fail")
def test_retry_weather_api_call_fail():
    with pytest.raises(TimeoutError):
        services.weather.get_weather("London")

