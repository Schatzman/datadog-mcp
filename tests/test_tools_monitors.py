"""Tests for monitors tools with mocked API."""

import json
from unittest.mock import MagicMock, patch

import pytest

from datadog_mcp.tools import monitors


def _monitor_like(**kwargs):
    """Object with model_dump()/to_dict() for _monitor_to_dict."""
    m = MagicMock()
    m.model_dump.return_value = kwargs
    m.to_dict.return_value = kwargs
    return m


def test_list_monitors_returns_json_array(mock_dd_env):
    """list_monitors returns JSON array of monitor-like objects."""
    fake = [_monitor_like(id=1, name="CPU", type="metric alert")]
    with patch("datadog_mcp.tools.monitors._api") as mock_api:
        mock_api.return_value.list_monitors.return_value = fake
        result = monitors.list_monitors()
    data = json.loads(result)
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "CPU"
    assert data[0]["id"] == 1


def test_get_monitor_returns_json_object(mock_dd_env):
    """get_monitor returns single monitor JSON."""
    fake = _monitor_like(id=42, name="Disk", type="metric alert", query="avg:system.disk.used")
    with patch("datadog_mcp.tools.monitors._api") as mock_api:
        mock_api.return_value.get_monitor.return_value = fake
        result = monitors.get_monitor(42)
    data = json.loads(result)
    assert data["id"] == 42
    assert data["name"] == "Disk"


def test_list_monitors_returns_error_on_api_exception(mock_dd_env):
    """list_monitors returns {\"error\": ...} on API failure."""
    from datadog_api_client.exceptions import ApiException

    with patch("datadog_mcp.tools.monitors._api") as mock_api:
        mock_api.return_value.list_monitors.side_effect = ApiException(status=403, reason="Forbidden")
        result = monitors.list_monitors()
    data = json.loads(result)
    assert "error" in data
    assert "403" in data["error"] or "permission" in data["error"].lower() or "Forbidden" in data["error"]
