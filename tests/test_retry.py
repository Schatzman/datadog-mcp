"""Tests for 429 retry with backoff."""

from unittest.mock import patch

import pytest

from datadog_api_client.configuration import Configuration
from datadog_api_client.exceptions import ApiException

from datadog_mcp.retry import RetryingApiClient


def test_retrying_client_returns_on_success(mock_dd_env):
    """First call succeeds; no retry."""
    config = Configuration()
    config.api_key["apiKeyAuth"] = "test"
    config.api_key["appKeyAuth"] = "test"
    client = RetryingApiClient(config, max_retries=2)
    with patch("datadog_mcp.retry.ApiClient.call_api", return_value={"valid": True}) as m:
        out = client.call_api("/api/v1/validate", "GET", response_type=(dict,))
    assert out == {"valid": True}
    assert m.call_count == 1


def test_retrying_client_retries_on_429_then_succeeds(mock_dd_env):
    """First call returns 429, second succeeds."""
    config = Configuration()
    config.api_key["apiKeyAuth"] = "test"
    config.api_key["appKeyAuth"] = "test"
    client = RetryingApiClient(config, max_retries=2, initial_backoff_sec=0.01)
    call_count = 0

    def side_effect(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            e = ApiException(status=429, reason="Too Many Requests")
            raise e
        return {"valid": True}

    with patch("datadog_mcp.retry.ApiClient.call_api", side_effect=side_effect):
        out = client.call_api("/api/v1/validate", "GET", response_type=(dict,))
    assert out == {"valid": True}
    assert call_count == 2


def test_retrying_client_raises_after_max_retries(mock_dd_env):
    """429 every time; raise after max retries."""
    config = Configuration()
    config.api_key["apiKeyAuth"] = "test"
    config.api_key["appKeyAuth"] = "test"
    client = RetryingApiClient(config, max_retries=2, initial_backoff_sec=0.01)

    def always_429(*args, **kwargs):
        raise ApiException(status=429, reason="Too Many Requests")

    with patch("datadog_mcp.retry.ApiClient.call_api", side_effect=always_429):
        with pytest.raises(ApiException) as exc_info:
            client.call_api("/api/v1/validate", "GET", response_type=(dict,))
    assert exc_info.value.status == 429


def test_retrying_client_does_not_retry_on_403(mock_dd_env):
    """403 is not retried."""
    config = Configuration()
    config.api_key["apiKeyAuth"] = "test"
    config.api_key["appKeyAuth"] = "test"
    client = RetryingApiClient(config, max_retries=2)

    def raise_403(*args, **kwargs):
        raise ApiException(status=403, reason="Forbidden")

    with patch("datadog_mcp.retry.ApiClient.call_api", side_effect=raise_403):
        with pytest.raises(ApiException) as exc_info:
            client.call_api("/api/v1/validate", "GET", response_type=(dict,))
    assert exc_info.value.status == 403
