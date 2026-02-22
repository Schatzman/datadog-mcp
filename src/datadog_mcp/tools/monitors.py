"""
Monitors API tools. DataDog API: https://docs.datadoghq.com/api/latest/monitors/
Scopes: monitors_read, monitors_write (for create/update/mute).
"""

import json
from typing import Any

from datadog_api_client.v1.api.monitors_api import MonitorsApi
from datadog_api_client.v1.model.monitor import Monitor
from datadog_api_client.v1.model.monitor_options import MonitorOptions
from datadog_api_client.v1.model.monitor_update_request import MonitorUpdateRequest
from datadog_api_client.exceptions import ApiException

from ..client import get_api_client
from ..errors import sanitize_error


def _api() -> MonitorsApi:
    return MonitorsApi(get_api_client())


def list_monitors(
    group_states: str | None = None,
    name: str | None = None,
    tags: str | None = None,
    monitor_tags: str | None = None,
    with_downtimes: bool | None = None,
    page: int | None = None,
    page_size: int | None = None,
) -> str:
    """List monitors. GET /api/v1/monitor. Optional filters: group_states, name, tags, monitor_tags, with_downtimes, page, page_size."""
    try:
        api = _api()
        monitors = api.list_monitors(
            group_states=group_states or None,
            name=name or None,
            tags=tags or None,
            monitor_tags=monitor_tags or None,
            with_downtimes=with_downtimes,
            page=page,
            page_size=page_size or None,
        )
        return json.dumps([_monitor_to_dict(m) for m in monitors])
    except ApiException as e:
        return json.dumps({"error": sanitize_error(e)})


def get_monitor(monitor_id: int, with_downtimes: bool = False) -> str:
    """Get a single monitor by ID. GET /api/v1/monitor/{monitor_id}."""
    try:
        api = _api()
        m = api.get_monitor(monitor_id, with_downtimes=with_downtimes)
        return json.dumps(_monitor_to_dict(m))
    except ApiException as e:
        return json.dumps({"error": sanitize_error(e)})


def create_monitor(body_json: str) -> str:
    """Create a monitor. POST /api/v1/monitor. body_json: JSON object with type, query, name, message, etc. Scope: monitors_write."""
    try:
        api = _api()
        body = json.loads(body_json)
        m = api.create_monitor(body=Monitor(**body))
        return json.dumps(_monitor_to_dict(m))
    except json.JSONDecodeError as e:
        return json.dumps({"error": f"Invalid JSON: {e!s}"})
    except ApiException as e:
        return json.dumps({"error": sanitize_error(e)})


def mute_monitor(monitor_id: int) -> str:
    """Mute a monitor (set silenced to *). PATCH via update. Scope: monitors_write."""
    try:
        api = _api()
        current = api.get_monitor(monitor_id)
        opts = getattr(current, "options", None) or MonitorOptions()
        opts_dict = opts.to_dict() if hasattr(opts, "to_dict") else {}
        opts_dict["silenced"] = {"*": None}
        update = MonitorUpdateRequest(options=MonitorOptions(**opts_dict))
        api.update_monitor(monitor_id, body=update)
        return json.dumps({"ok": True, "monitor_id": monitor_id, "message": "Monitor muted."})
    except ApiException as e:
        return json.dumps({"error": sanitize_error(e)})


def unmute_monitor(monitor_id: int) -> str:
    """Unmute a monitor (clear silenced). PATCH via update. Scope: monitors_write."""
    try:
        api = _api()
        update = MonitorUpdateRequest(options=MonitorOptions(silenced={}))
        api.update_monitor(monitor_id, body=update)
        return json.dumps({"ok": True, "monitor_id": monitor_id, "message": "Monitor unmuted."})
    except ApiException as e:
        return json.dumps({"error": sanitize_error(e)})


def update_monitor(monitor_id: int, body_json: str) -> str:
    """Update a monitor. PATCH /api/v1/monitor/{id}. body_json: JSON with optional name, message, query, options, tags, etc. Scope: monitors_write."""
    try:
        api = _api()
        body = json.loads(body_json)
        update = MonitorUpdateRequest(**body)
        m = api.update_monitor(monitor_id, body=update)
        return json.dumps(_monitor_to_dict(m))
    except json.JSONDecodeError as e:
        return json.dumps({"error": f"Invalid JSON: {e!s}"})
    except ApiException as e:
        return json.dumps({"error": sanitize_error(e)})


def delete_monitor(monitor_id: int) -> str:
    """Delete a monitor. DELETE /api/v1/monitor/{id}. Scope: monitors_write."""
    try:
        api = _api()
        result = api.delete_monitor(monitor_id)
        out = getattr(result, "deleted_monitor_id", monitor_id)
        return json.dumps({"ok": True, "deleted_monitor_id": out})
    except ApiException as e:
        return json.dumps({"error": sanitize_error(e)})


def _monitor_to_dict(m: Any) -> dict:
    """Convert Monitor object to JSON-serializable dict."""
    if hasattr(m, "model_dump"):
        return m.model_dump()
    if hasattr(m, "to_dict"):
        return m.to_dict()
    return {"id": getattr(m, "id", None), "name": getattr(m, "name", None), "type": getattr(m, "type", None)}
