"""Tests for MCP resources (datadog:// URIs) with mocked API."""

import json
from unittest.mock import patch

import pytest

from datadog_mcp.resources import (
    get_dashboard_by_id,
    get_dashboards_list,
    get_monitor_by_id,
    get_monitors_list,
)


def test_get_monitors_list_returns_json(mock_dd_env):
    """datadog://monitors returns JSON list."""
    with patch("datadog_mcp.resources.monitors.list_monitors", return_value='[{"id": 1, "name": "M1"}]'):
        result = get_monitors_list()
    data = json.loads(result)
    assert isinstance(data, list)
    assert data[0]["name"] == "M1"


def test_get_monitor_by_id_returns_json(mock_dd_env):
    """datadog://monitors/{id} returns JSON object."""
    with patch("datadog_mcp.resources.monitors.get_monitor", return_value='{"id": 2, "name": "M2"}'):
        result = get_monitor_by_id("2")
    data = json.loads(result)
    assert data["id"] == 2
    assert data["name"] == "M2"


def test_get_dashboards_list_returns_json(mock_dd_env):
    """datadog://dashboards returns JSON list."""
    with patch("datadog_mcp.resources.dashboards.list_dashboards", return_value='[{"id": "abc", "title": "DB"}]'):
        result = get_dashboards_list()
    data = json.loads(result)
    assert isinstance(data, list)
    assert data[0]["title"] == "DB"


def test_get_dashboard_by_id_returns_json(mock_dd_env):
    """datadog://dashboards/{id} returns JSON object."""
    with patch("datadog_mcp.resources.dashboards.get_dashboard", return_value='{"id": "xyz", "title": "Dash"}'):
        result = get_dashboard_by_id("xyz")
    data = json.loads(result)
    assert data["id"] == "xyz"
    assert data["title"] == "Dash"
