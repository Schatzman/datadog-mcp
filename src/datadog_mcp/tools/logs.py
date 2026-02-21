"""
Logs API tools. DataDog API: https://docs.datadoghq.com/api/v1/logs/ and logs-indexes.
Scopes: logs_read_config (indexes), logs_read (list/query).
"""

import json
from datetime import datetime, timezone
from typing import Any

from datadog_api_client.v1.api.logs_api import LogsApi
from datadog_api_client.v1.api.logs_indexes_api import LogsIndexesApi
from datadog_api_client.v1.model.logs_list_request import LogsListRequest
from datadog_api_client.v1.model.logs_list_request_time import LogsListRequestTime
from datadog_api_client.v1.model.logs_sort import LogsSort
from datadog_api_client.exceptions import ApiException

from ..client import get_api_client
from ..errors import sanitize_error


def _logs_api() -> LogsApi:
    return LogsApi(get_api_client())


def _indexes_api() -> LogsIndexesApi:
    return LogsIndexesApi(get_api_client())


def list_log_indexes() -> str:
    """List log indexes. GET /api/v1/logs/config/indexes."""
    try:
        api = _indexes_api()
        indexes = api.list_log_indexes()
        return json.dumps(_indexes_to_list(indexes))
    except ApiException as e:
        return json.dumps({"error": sanitize_error(e)})


def query_logs(
    start_ts: int,
    end_ts: int,
    query: str | None = None,
    limit: int = 50,
    sort: str = "desc",
    index: str | None = None,
) -> str:
    """Query logs in a time range. POST /api/v1/logs-queries/list. start_ts/end_ts in Unix seconds."""
    try:
        start_dt = datetime.fromtimestamp(start_ts, tz=timezone.utc)
        end_dt = datetime.fromtimestamp(end_ts, tz=timezone.utc)
        time_obj = LogsListRequestTime(_from=start_dt, to=end_dt)
        sort_enum = LogsSort.TIME_DESCENDING if sort == "desc" else LogsSort.TIME_ASCENDING
        body = LogsListRequest(time=time_obj, limit=limit, sort=sort_enum, query=query, index=index)
        api = _logs_api()
        resp = api.list_logs(body=body)
        return json.dumps(_logs_list_response_to_dict(resp))
    except ApiException as e:
        return json.dumps({"error": sanitize_error(e)})


def _indexes_to_list(idx: Any) -> list:
    if idx is None:
        return []
    raw = idx.indexes if hasattr(idx, "indexes") else (idx if isinstance(idx, list) else [])
    return [i.to_dict() if hasattr(i, "to_dict") else str(i) for i in raw]


def _logs_list_response_to_dict(r: Any) -> dict:
    if hasattr(r, "to_dict"):
        return r.to_dict()
    return {"logs": getattr(r, "logs", []), "next_log_id": getattr(r, "next_log_id", None), "status": getattr(r, "status", None)}
