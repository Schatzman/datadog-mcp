"""
Metrics API tools. DataDog API: https://docs.datadoghq.com/api/v1/metrics/
Scopes: metrics_read, metrics_write (for submit).
"""

import json
from typing import Any

from datadog_api_client.v1.api.metrics_api import MetricsApi
from datadog_api_client.exceptions import ApiException

from ..client import get_api_client
from ..errors import sanitize_error


def _api() -> MetricsApi:
    return MetricsApi(get_api_client())


def query_metrics(from_ts: int, to_ts: int, query: str) -> str:
    """Query metrics in a time range. GET /api/v1/query. from_ts and to_ts are Unix seconds."""
    try:
        api = _api()
        resp = api.query_metrics(_from=from_ts, to=to_ts, query=query)
        return json.dumps(_query_response_to_dict(resp))
    except ApiException as e:
        return json.dumps({"error": sanitize_error(e)})


def _query_response_to_dict(r: Any) -> dict:
    if hasattr(r, "to_dict"):
        return r.to_dict()
    return {"series": getattr(r, "series", []), "from_date": getattr(r, "from_date", None), "to_date": getattr(r, "to_date", None)}
