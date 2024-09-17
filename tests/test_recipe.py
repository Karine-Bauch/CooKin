import pytest

import services.recipe
import services.weather


@pytest.mark.usefixtures("mock_get_weather")
def test_recipe():
    recipe = services.recipe.get_recipe("Paris")
    assert isinstance(recipe, str)
    assert len(recipe) > 0


def test_weather():
    weather = services.weather.get_weather("London")
    assert isinstance(weather, dict)
    assert weather["nearest_area"][0]["country"][0]["value"]
    assert weather["current_condition"][0]["weatherDesc"][0]["value"]
    assert weather["current_condition"][0]["temp_C"]
    assert weather["current_condition"][0]["humidity"]
    assert weather["current_condition"][0]["windspeedKmph"]
    assert weather["nearest_area"][0]["country"][0]["value"] == "United Kingdom"
