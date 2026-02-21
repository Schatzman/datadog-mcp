"""
Service Level Objectives API. DataDog API: https://docs.datadoghq.com/api/v1/service-level-objectives/
Scopes: slo_read.
"""

import json
from typing import Any

from datadog_api_client.v1.api.service_level_objectives_api import ServiceLevelObjectivesApi
from datadog_api_client.exceptions import ApiException

from ..client import get_api_client
from ..errors import sanitize_error


def _api() -> ServiceLevelObjectivesApi:
    return ServiceLevelObjectivesApi(get_api_client())


def list_slos(
    ids: str | None = None,
    query: str | None = None,
    tags_query: str | None = None,
    metrics_query: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
) -> str:
    """List SLOs. GET /api/v1/slo. Optional: ids, query, tags_query, metrics_query, limit, offset."""
    try:
        api = _api()
        resp = api.list_slos(
            ids=ids,
            query=query,
            tags_query=tags_query,
            metrics_query=metrics_query,
            limit=limit,
            offset=offset,
        )
        return json.dumps(_slo_list_to_dict(resp))
    except ApiException as e:
        return json.dumps({"error": sanitize_error(e)})


def get_slo(slo_id: str, with_configured_alert_ids: bool = False) -> str:
    """Get a single SLO by ID. GET /api/v1/slo/{slo_id}."""
    try:
        api = _api()
        resp = api.get_slo(slo_id, with_configured_alert_ids=with_configured_alert_ids)
        return json.dumps(_slo_response_to_dict(resp))
    except ApiException as e:
        return json.dumps({"error": sanitize_error(e)})


def _slo_list_to_dict(r: Any) -> dict:
    if hasattr(r, "to_dict"):
        return r.to_dict()
    return {"data": getattr(r, "data", [])}


def _slo_response_to_dict(r: Any) -> dict:
    if hasattr(r, "to_dict"):
        return r.to_dict()
    return {}
