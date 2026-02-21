"""Tests for config module: env loading and validation."""

import pytest

from datadog_mcp.config import get_config


def test_get_config_raises_when_api_key_missing(clean_env):
    with pytest.raises(ValueError) as exc_info:
        get_config()
    assert "DD_API_KEY" in str(exc_info.value)


def test_get_config_raises_when_app_key_missing(clean_env, monkeypatch):
    monkeypatch.setenv("DD_API_KEY", "abc")
    with pytest.raises(ValueError) as exc_info:
        get_config()
    assert "DD_APP_KEY" in str(exc_info.value)


def test_get_config_returns_dict_when_both_set(clean_env, monkeypatch):
    monkeypatch.setenv("DD_API_KEY", "api123")
    monkeypatch.setenv("DD_APP_KEY", "app456")
    cfg = get_config()
    assert cfg["api_key"] == "api123"
    assert cfg["app_key"] == "app456"
    assert cfg["site"] == "datadoghq.com"


def test_get_config_uses_dd_site_when_set(clean_env, monkeypatch):
    monkeypatch.setenv("DD_API_KEY", "a")
    monkeypatch.setenv("DD_APP_KEY", "b")
    monkeypatch.setenv("DD_SITE", "datadoghq.eu")
    cfg = get_config()
    assert cfg["site"] == "datadoghq.eu"
