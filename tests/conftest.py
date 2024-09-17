import pytest


FAKE_WEATHER = {
            "current_condition": [
                {
                    "humidity": "73",
                    "temp_C": "18",
                    "weatherDesc": [
                        {
                            "value": "Partly cloudy"
                        }
                    ],
                    "windspeedKmph": "22",
                }
            ],
            "nearest_area": [
                {
                    "country": [
                        {
                            "value": "France"
                        }
                    ],
                }
            ],
        }

@pytest.fixture
def mock_get_weather(mocker) -> None:
    mocker.patch(
        "services.weather.get_weather",
        return_value=FAKE_WEATHER
    )