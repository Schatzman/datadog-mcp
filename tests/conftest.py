"""Pytest fixtures: mock DataDog client and env."""

import os
from unittest.mock import patch

import pytest


@pytest.fixture(autouse=True)
def clean_env(monkeypatch):
    """Ensure tests don't accidentally use real DD keys from env."""
    for key in ("DD_API_KEY", "DD_APP_KEY", "DD_SITE"):
        monkeypatch.delenv(key, raising=False)


@pytest.fixture
def mock_dd_env(monkeypatch):
    """Set fake DD env vars so get_config() succeeds."""
    monkeypatch.setenv("DD_API_KEY", "test_api_key")
    monkeypatch.setenv("DD_APP_KEY", "test_app_key")
    monkeypatch.setenv("DD_SITE", "datadoghq.com")
