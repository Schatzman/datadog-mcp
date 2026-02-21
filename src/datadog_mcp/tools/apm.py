"""
APM API (v2). DataDog API: https://docs.datadoghq.com/api/latest/apm/
Scopes: apm_read.
"""

import json
from typing import Any

from datadog_api_client.v2.api.apm_api import APMApi
from datadog_api_client.exceptions import ApiException

from ..client import get_api_client
from ..errors import sanitize_error


def _api() -> APMApi:
    return APMApi(get_api_client())


def list_apm_services(filter_env: str = "*") -> str:
    """List APM services. GET /api/v2/apm/services. filter_env: environment filter, use '*' for all. Scope: apm_read."""
    try:
        api = _api()
        resp = api.get_service_list(filter_env=filter_env)
        return json.dumps(_service_list_to_dict(resp))
    except ApiException as e:
        return json.dumps({"error": sanitize_error(e)})


def _service_list_to_dict(r: Any) -> dict:
    if hasattr(r, "to_dict"):
        return r.to_dict()
    return {"data": getattr(r, "data", [])}
