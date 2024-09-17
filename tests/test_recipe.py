import pytest

import services.recipe
import services.weather

import pytest


@pytest.mark.usefixtures("mock_get_weather")
def test_recipe():
    recipe = services.recipe.get_recipe("Paris")
    assert isinstance(recipe, str)
    assert len(recipe) > 0


def test_weather():
    weather = services.weather.get_weather("London")
    assert isinstance(weather, dict)
    assert weather["nearest_area"][0]["country"][0]["value"] == "United Kingdom"
