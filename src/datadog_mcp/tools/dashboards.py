"""
Dashboards API tools. DataDog API: https://docs.datadoghq.com/api/latest/dashboards/
Scopes: dashboards_read, dashboards_write (for create/update/delete).
"""

import json
from typing import Any

from datadog_api_client.v1.api.dashboards_api import DashboardsApi
from datadog_api_client.v1.model.dashboard import Dashboard
from datadog_api_client.exceptions import ApiException

from ..client import get_api_client
from ..errors import sanitize_error


def _api() -> DashboardsApi:
    return DashboardsApi(get_api_client())


def list_dashboards(
    filter_shared: bool | None = None,
    filter_deleted: bool | None = None,
    count: int | None = None,
    start: int | None = None,
) -> str:
    """List dashboards. GET /api/v1/dashboard. Optional: filter_shared, filter_deleted, count, start."""
    try:
        api = _api()
        summary = api.list_dashboards(
            filter_shared=filter_shared,
            filter_deleted=filter_deleted,
            count=count,
            start=start,
        )
        return json.dumps(_dashboard_summary_to_dict(summary))
    except ApiException as e:
        return json.dumps({"error": sanitize_error(e)})


def get_dashboard(dashboard_id: str) -> str:
    """Get a single dashboard by ID. GET /api/v1/dashboard/{dashboard_id}."""
    try:
        api = _api()
        d = api.get_dashboard(dashboard_id)
        return json.dumps(_dashboard_to_dict(d))
    except ApiException as e:
        return json.dumps({"error": sanitize_error(e)})


def create_dashboard(body_json: str) -> str:
    """Create a dashboard. POST /api/v1/dashboard. body_json: JSON with title, widgets, layout_type, etc. Scope: dashboards_write."""
    try:
        api = _api()
        body = json.loads(body_json)
        d = api.create_dashboard(body=Dashboard(**body))
        return json.dumps(_dashboard_to_dict(d))
    except json.JSONDecodeError as e:
        return json.dumps({"error": f"Invalid JSON: {e!s}"})
    except ApiException as e:
        return json.dumps({"error": sanitize_error(e)})


def update_dashboard(dashboard_id: str, body_json: str) -> str:
    """Update a dashboard. PUT /api/v1/dashboard/{dashboard_id}. Scope: dashboards_write."""
    try:
        api = _api()
        body = json.loads(body_json)
        d = api.update_dashboard(dashboard_id, body=Dashboard(**body))
        return json.dumps(_dashboard_to_dict(d))
    except json.JSONDecodeError as e:
        return json.dumps({"error": f"Invalid JSON: {e!s}"})
    except ApiException as e:
        return json.dumps({"error": sanitize_error(e)})


def delete_dashboard(dashboard_id: str) -> str:
    """Delete a dashboard. DELETE /api/v1/dashboard/{dashboard_id}. Scope: dashboards_write."""
    try:
        api = _api()
        api.delete_dashboard(dashboard_id)
        return json.dumps({"ok": True, "dashboard_id": dashboard_id, "message": "Dashboard deleted."})
    except ApiException as e:
        return json.dumps({"error": sanitize_error(e)})


def _dashboard_summary_to_dict(s: Any) -> dict:
    if hasattr(s, "to_dict"):
        return s.to_dict()
    return {"dashboards": getattr(s, "dashboards", [])}


def _dashboard_to_dict(d: Any) -> dict:
    if hasattr(d, "to_dict"):
        return d.to_dict()
    return dict(d) if hasattr(d, "__iter__") else {}
