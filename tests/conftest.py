import httpx
import openai
import pytest
import unittest.mock

from openai.types import CompletionUsage
from openai.types.chat import ChatCompletion, ChatCompletionMessage
from openai.types.chat.chat_completion import Choice
from openai.types.completion_usage import CompletionTokensDetails


fake_completion: ChatCompletion = ChatCompletion(
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


fake_weather: dict = {
    "current_condition": [
        {
            "humidity": "73",
            "temp_C": "18",
            "weatherDesc": [{"value": "Partly cloudy"}],
            "windspeedKmph": "22",
        }
    ],
}


### SUCCESS MOCK ###

mock_weather_success = unittest.mock.Mock(spec=httpx.Response)
mock_weather_success.status_code = 200
mock_weather_success.json.return_value = {
    "current_condition": [
        {
            "humidity": "73",
            "temp_C": "18",
            "weatherDesc": [{"value": "Partly cloudy"}],
            "windspeedKmph": "22",
        }
    ],
}

mock_response_success = unittest.mock.Mock(spec=httpx.Response)
mock_response_success.status_code = 200
mock_response_success.json.return_value = {
    "place_id": 243407805,
}


@pytest.fixture
def mock_open_streetmap_api_call_success(mocker) -> None:
    mocker.patch("services.weather.httpx.get", return_value=mock_response_success)


@pytest.fixture
def mock_weather_api_call_success(mocker) -> None:
    mocker.patch("services.weather.httpx.get", return_value=mock_weather_success)


@pytest.fixture
def mock_openai_api_call_success(mocker) -> None:
    mocker.patch("services.recipe.openai_api_call", return_value=fake_completion)


### FAIL MOCK ###

mock_response_fail = unittest.mock.Mock(spec=httpx.Response)
mock_response_fail.status_code = 400
mock_response_fail.raise_for_status.side_effect = httpx.HTTPStatusError(
    message="Not Found",
    request=httpx.Request("GET", "https://example.com"),
    response=mock_response_fail,
)


@pytest.fixture
def mock_open_streetmap_api_call_fail(mocker) -> None:
    mocker.patch("services.weather.httpx.get", return_value=mock_response_fail)


@pytest.fixture
def mock_weather_api_call_fail(mocker) -> None:
    mocker.patch("services.weather.httpx.get", side_effect=httpx.TimeoutException("Timeout"))


@pytest.fixture
def mock_openai_api_call_fail(mocker) -> None:
    mocker.patch(
        "services.recipe.openai_api_call",
        side_effect=openai.APITimeoutError(request=httpx.Request("GET", "https://example.com"))
    )
