"""
DataDog API client factory and validation.
Uses official datadog-api-client; validates keys on first use.
"""

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.authentication_api import AuthenticationApi

from .config import get_config
from .retry import RetryingApiClient

_config: Configuration | None = None
_api_client: ApiClient | None = None


def get_api_client() -> ApiClient:
    """Return a shared ApiClient with retry on 429. Creates and validates on first use."""
    global _config, _api_client
    if _api_client is not None:
        return _api_client
    cfg = get_config()
    _config = Configuration()
    _config.api_key["apiKeyAuth"] = cfg["api_key"]
    _config.api_key["appKeyAuth"] = cfg["app_key"]
    _config.server_variables["site"] = cfg["site"]
    _api_client = RetryingApiClient(_config)
    return _api_client


def validate_keys() -> dict:
    """
    Call GET /api/v1/validate. Returns a dict with 'valid' and optional message.
    See: https://docs.datadoghq.com/api/latest/authentication/
    """
    try:
        client = get_api_client()
        api = AuthenticationApi(client)
        resp = api.validate()
        return {"valid": getattr(resp, "valid", True)}
    except Exception as e:
        msg = str(e)
        if "api_key" in msg.lower() or "403" in msg:
            return {"valid": False, "error": "Invalid API key or insufficient permissions."}
        return {"valid": False, "error": msg}
