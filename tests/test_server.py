"""Tests for server: tools and resources are registered."""

import json
from unittest.mock import patch

import pytest

from datadog_mcp.server import validate_keys_tool


def test_validate_keys_tool_returns_json(mock_dd_env):
    with patch("datadog_mcp.server.validate_keys", return_value={"valid": True}):
        result = validate_keys_tool()
    out = json.loads(result)
    assert out["valid"] is True


def test_validate_keys_tool_returns_valid_false_on_error(mock_dd_env):
    with patch(
        "datadog_mcp.server.validate_keys",
        return_value={"valid": False, "error": "Invalid API key"},
    ):
        result = validate_keys_tool()
    out = json.loads(result)
    assert out["valid"] is False
    assert "error" in out


def test_server_has_tools():
    assert callable(validate_keys_tool)
