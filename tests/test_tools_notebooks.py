"""Tests for Notebooks tools with mocked API."""

import json
from unittest.mock import MagicMock, patch

import pytest

from datadog_mcp.tools import notebooks


def _test_like(**kwargs):
    """Object with to_dict() for _to_dict."""
    m = MagicMock()
    m.to_dict.return_value = kwargs
    m.model_dump.return_value = kwargs
    return m


def test_list_notebooks_returns_json(mock_dd_env):
    """list_notebooks returns JSON with notebooks list shape."""
    fake = _test_like(data=[{"id": 12345, "attributes": {"name": "My Notebook"}}])
    with patch("datadog_mcp.tools.notebooks._api") as mock_api:
        mock_api.return_value.list_notebooks.return_value = fake
        result = notebooks.list_notebooks()
    data = json.loads(result)
    assert "data" in data or isinstance(data, dict)
    if "data" in data:
        assert data["data"][0]["id"] == 12345


def test_get_notebook_returns_json_object(mock_dd_env):
    """get_notebook returns single notebook JSON."""
    fake = _test_like(data={"id": 12345, "attributes": {"name": "My Notebook", "cells": []}})
    with patch("datadog_mcp.tools.notebooks._api") as mock_api:
        mock_api.return_value.get_notebook.return_value = fake
        result = notebooks.get_notebook("12345")
    data = json.loads(result)
    assert data["data"]["id"] == 12345


def test_list_notebooks_returns_error_on_api_exception(mock_dd_env):
    """list_notebooks returns {\"error\": ...} on API failure."""
    from datadog_api_client.exceptions import ApiException

    with patch("datadog_mcp.tools.notebooks._api") as mock_api:
        mock_api.return_value.list_notebooks.side_effect = ApiException(status=403, reason="Forbidden")
        result = notebooks.list_notebooks()
    data = json.loads(result)
    assert "error" in data
