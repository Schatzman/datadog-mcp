"""
Events API tools. DataDog API: https://docs.datadoghq.com/api/v1/events/
Scopes: events_read, events_write (for create).
"""

import json
from typing import Any

from datadog_api_client.v1.api.events_api import EventsApi
from datadog_api_client.exceptions import ApiException

from ..client import get_api_client
from ..errors import sanitize_error


def _api() -> EventsApi:
    return EventsApi(get_api_client())


def list_events(
    start_ts: int,
    end_ts: int,
    priority: str | None = None,
    sources: str | None = None,
    tags: str | None = None,
    page: int | None = None,
) -> str:
    """List events in a time range. GET /api/v1/events. start_ts/end_ts in Unix seconds."""
    try:
        api = _api()
        resp = api.list_events(
            start=start_ts,
            end=end_ts,
            priority=priority,
            sources=sources,
            tags=tags,
            page=page,
        )
        return json.dumps(_event_list_response_to_dict(resp))
    except ApiException as e:
        return json.dumps({"error": sanitize_error(e)})


def _event_list_response_to_dict(r: Any) -> dict:
    if hasattr(r, "to_dict"):
        return r.to_dict()
    return {"events": getattr(r, "events", []), "status": getattr(r, "status", None)}
