import pytest
from openai.types import CompletionUsage
from openai.types.chat import ChatCompletion, ChatCompletionMessage
from openai.types.chat.chat_completion import Choice
from openai.types.completion_usage import CompletionTokensDetails

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

fake_completion = ChatCompletion(
    id="chatcmpl-A8qL8QM2P9R61wVlaKxFy54QfA1FG",
    choices=[
        Choice(
            finish_reason="stop",
            index=0,
            logprobs=None,
            message=ChatCompletionMessage(
                content="This a fake recipe",
                refusal=None,
                role="assistant",
                function_call=None,
                tool_calls=None,
            ),
        )
    ],
    created=1726671182,
    model="gpt-4o-mini-2024-07-18",
    object="chat.completion",
    service_tier=None,
    system_fingerprint="fp_483d39d857",
    usage=CompletionUsage(
        completion_tokens=569,
        prompt_tokens=79,
        total_tokens=648,
        completion_tokens_details=CompletionTokensDetails(reasoning_tokens=0),
    ),
)


@pytest.fixture
def mock_get_weather(mocker) -> None:
    mocker.patch("services.weather.get_weather", return_value=fake_weather)


@pytest.fixture
def mock_api_call(mocker) -> None:
    mocker.patch("services.weather.weather_api_call", return_value=fake_weather)
    mocker.patch("services.recipe.openai_api_call", return_value=fake_completion)


@pytest.fixture
def mock_api_call_fail(mocker) -> None:
    mocker.patch("services.weather.weather_api_call", return_value=None)
    mocker.patch("services.recipe.openai_api_call", return_value=None)
