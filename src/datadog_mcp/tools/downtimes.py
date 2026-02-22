"""
Downtimes API (v1). DataDog API: https://docs.datadoghq.com/api/latest/downtimes/
Scopes: monitors_read (list/get), monitors_write (create/update/cancel).
"""

import json
from typing import Any

from datadog_api_client.v1.api.downtimes_api import DowntimesApi
from datadog_api_client.v1.model.downtime import Downtime
from datadog_api_client.exceptions import ApiException

from ..client import get_api_client
from ..errors import sanitize_error


def _api() -> DowntimesApi:
    return DowntimesApi(get_api_client())


def _downtime_to_dict(d: Any) -> dict:
    """Convert Downtime to JSON-serializable dict."""
    if hasattr(d, "to_dict"):
        return d.to_dict()
    if hasattr(d, "model_dump"):
        return d.model_dump()
    return dict(d) if hasattr(d, "items") else {"id": getattr(d, "id", None)}


def list_downtimes(
    current_only: bool | None = None,
    with_creator: bool | None = None,
) -> str:
    """List downtimes. GET /api/v1/downtime. Optional: current_only, with_creator. Scope: monitors_read."""
    try:
        api = _api()
        result = api.list_downtimes(
            current_only=current_only,
            with_creator=with_creator,
        )
        if result is None:
            return json.dumps([])
        items = result if isinstance(result, list) else [result]
        return json.dumps([_downtime_to_dict(x) for x in items])
    except ApiException as e:
        return json.dumps({"error": sanitize_error(e)})


def get_downtime(downtime_id: int) -> str:
    """Get a single downtime by ID. GET /api/v1/downtime/{id}. Scope: monitors_read."""
    try:
        api = _api()
        d = api.get_downtime(downtime_id)
        return json.dumps(_downtime_to_dict(d))
    except ApiException as e:
        return json.dumps({"error": sanitize_error(e)})


def create_downtime(body_json: str) -> str:
    """Create a downtime. POST /api/v1/downtime. body_json: JSON with scope (list), start (int), optional end, message, monitor_id, etc. Scope: monitors_write."""
    try:
        api = _api()
        body = json.loads(body_json)
        d = api.create_downtime(body=Downtime(**body))
        return json.dumps(_downtime_to_dict(d))
    except json.JSONDecodeError as e:
        return json.dumps({"error": f"Invalid JSON: {e!s}"})
    except ApiException as e:
        return json.dumps({"error": sanitize_error(e)})


def update_downtime(downtime_id: int, body_json: str) -> str:
    """Update a downtime. PATCH /api/v1/downtime/{id}. body_json: JSON with optional scope, start, end, message, etc. Scope: monitors_write."""
    try:
        api = _api()
        body = json.loads(body_json)
        d = api.update_downtime(downtime_id, body=Downtime(**body))
        return json.dumps(_downtime_to_dict(d))
    except json.JSONDecodeError as e:
        return json.dumps({"error": f"Invalid JSON: {e!s}"})
    except ApiException as e:
        return json.dumps({"error": sanitize_error(e)})


def cancel_downtime(downtime_id: int) -> str:
    """Cancel (delete) a downtime. DELETE /api/v1/downtime/{id}. Scope: monitors_write."""
    try:
        api = _api()
        api.cancel_downtime(downtime_id)
        return json.dumps({"ok": True, "downtime_id": downtime_id, "message": "Downtime canceled."})
    except ApiException as e:
        return json.dumps({"error": sanitize_error(e)})
