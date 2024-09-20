import httpx
import pytest

import services.exc
import services.recipe
import services.weather


@pytest.mark.usefixtures("mock_open_streetmap_api_call_success")
def test_check_city() -> None:
    services.weather.check_city("London")


@pytest.mark.usefixtures("mock_open_streetmap_api_call_fail")
def test_check_city_fail() -> None:
    with pytest.raises(httpx.HTTPStatusError):
        services.weather.check_city("Not a city")


@pytest.mark.usefixtures("mock_weather_api_call_success")
def test_weather_has_needed_fields() -> None:
    weather = services.weather.get_weather("London")
    assert weather["current_condition"][0]["weatherDesc"][0]["value"]
    assert weather["current_condition"][0]["temp_C"]
    assert weather["current_condition"][0]["humidity"]
    assert weather["current_condition"][0]["windspeedKmph"]


@pytest.mark.usefixtures("mock_weather_api_call_success")
def test_prompt_creation() -> None:
    weather = services.weather.get_weather("London")
    prompt = services.recipe.create_prompt(
        weather["current_condition"][0]["weatherDesc"][0]["value"],
        weather["current_condition"][0]["temp_C"],
        weather["current_condition"][0]["humidity"],
        weather["current_condition"][0]["windspeedKmph"],
    )
    assert len(prompt) > 0
    assert weather["current_condition"][0]["weatherDesc"][0]["value"] in prompt
    assert weather["current_condition"][0]["temp_C"] in prompt
    assert weather["current_condition"][0]["humidity"] in prompt
    assert weather["current_condition"][0]["windspeedKmph"] in prompt


@pytest.mark.usefixtures(
    "mock_open_streetmap_api_call_success", "mock_weather_api_call_success"
)
def test_get_weather_success():
    weather = services.weather.get_weather("London")
    assert isinstance(weather, dict)


@pytest.mark.usefixtures(
    "mock_open_streetmap_api_call_success", "mock_weather_api_call_fail"
)
def test_get_weather_fail_with_retry():
    with pytest.raises(TimeoutError):
        services.weather.get_weather("London")


@pytest.mark.usefixtures(
    "mock_open_streetmap_api_call_success",
    "mock_weather_api_call_success",
    "mock_openai_api_call_success",
)
def test_get_recipe_success():
    completion = services.recipe.get_recipe("London")
    assert isinstance(completion, str)
    assert len(completion) > 0


@pytest.mark.usefixtures(
    "mock_open_streetmap_api_call_success",
    "mock_weather_api_call_success",
    "mock_openai_api_call_fail",
)
def test_get_recipe_with_retry():
    with pytest.raises(TimeoutError):
        services.recipe.get_recipe("London")
