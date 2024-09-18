import pytest

fake_weather: dict = {
    "current_condition": [
        {
            "humidity": "73",
            "temp_C": "18",
            "weatherDesc": [{"value": "Partly cloudy"}],
            "windspeedKmph": "22",
        }
    ],
    "nearest_area": [
        {
            "country": [{"value": "France"}],
        }
    ],
}


@pytest.fixture
def mock_get_weather(mocker) -> None:
    mocker.patch("services.weather.get_weather", return_value=fake_weather)


@pytest.fixture
def mock_weather_api_call(mocker) -> None:
    mocker.patch("services.weather.weather_api_call", return_value=fake_weather)


@pytest.fixture
def mock_weather_api_call_fail(mocker) -> None:
    mocker.patch("services.weather.weather_api_call", return_value=None)
