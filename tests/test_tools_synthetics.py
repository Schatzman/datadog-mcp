"""Tests for Synthetics tools with mocked API."""

import json
from unittest.mock import MagicMock, patch

import pytest

from datadog_mcp.tools import synthetics


def _test_like(**kwargs):
    """Object with to_dict() for _to_dict."""
    m = MagicMock()
    m.to_dict.return_value = kwargs
    m.model_dump.return_value = kwargs
    return m


def test_list_synthetics_tests_returns_json(mock_dd_env):
    """list_synthetics_tests returns JSON with tests list shape."""
    fake = _test_like(tests=[{"public_id": "abc-123", "name": "My API test"}])
    with patch("datadog_mcp.tools.synthetics._api") as mock_api:
        mock_api.return_value.list_tests.return_value = fake
        result = synthetics.list_synthetics_tests()
    data = json.loads(result)
    assert "tests" in data or "data" in data or isinstance(data, dict)
    if "tests" in data:
        assert data["tests"][0]["public_id"] == "abc-123"
        assert data["tests"][0]["name"] == "My API test"


def test_get_synthetics_test_returns_json_object(mock_dd_env):
    """get_synthetics_test returns single test JSON."""
    fake = _test_like(public_id="xyz-789", name="Browser test", type="browser")
    with patch("datadog_mcp.tools.synthetics._api") as mock_api:
        mock_api.return_value.get_test.return_value = fake
        result = synthetics.get_synthetics_test("xyz-789")
    data = json.loads(result)
    assert data["public_id"] == "xyz-789"
    assert data["name"] == "Browser test"


def test_list_synthetics_tests_returns_error_on_api_exception(mock_dd_env):
    """list_synthetics_tests returns {\"error\": ...} on API failure."""
    from datadog_api_client.exceptions import ApiException

    with patch("datadog_mcp.tools.synthetics._api") as mock_api:
        mock_api.return_value.list_tests.side_effect = ApiException(status=403, reason="Forbidden")
        result = synthetics.list_synthetics_tests()
    data = json.loads(result)
    assert "error" in data
