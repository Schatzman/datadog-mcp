"""
Notebooks API (v1). DataDog API: https://docs.datadoghq.com/api/latest/notebooks/
Scopes: notebooks_read.
"""

import json
from typing import Any

from datadog_api_client.v1.api.notebooks_api import NotebooksApi
from datadog_api_client.exceptions import ApiException

from ..client import get_api_client
from ..errors import sanitize_error


def _api() -> NotebooksApi:
    return NotebooksApi(get_api_client())


def _to_dict(obj: Any) -> dict:
    """Convert API response to dict for JSON serialization."""
    if hasattr(obj, "to_dict"):
        return obj.to_dict()
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    return {"data": getattr(obj, "data", [])}


def list_notebooks(
    count: int | None = None,
    start: int | None = None,
) -> str:
    """List notebooks. GET list endpoint. Optional: count, start. Scope: notebooks_read."""
    try:
        api = _api()
        kwargs = {}
        if count is not None:
            kwargs["count"] = count
        if start is not None:
            kwargs["start"] = start
        resp = api.list_notebooks(**kwargs)
        return json.dumps(_to_dict(resp))
    except ApiException as e:
        return json.dumps({"error": sanitize_error(e)})


def get_notebook(notebook_id: str) -> str:
    """Get a single notebook by notebook_id. GET notebook by id. Scope: notebooks_read."""
    try:
        api = _api()
        nid = int(notebook_id)
        resp = api.get_notebook(notebook_id=nid)
        return json.dumps(_to_dict(resp))
    except (ValueError, ApiException) as e:
        if isinstance(e, ApiException):
            return json.dumps({"error": sanitize_error(e)})
        return json.dumps({"error": "Invalid notebook_id: must be an integer."})
