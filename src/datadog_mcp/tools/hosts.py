"""
Hosts API tools. DataDog API: https://docs.datadoghq.com/api/v1/hosts/
Scopes: infrastructure_read. Tags: tags_read (TagsApi.get_host_tags).
"""

import json
from typing import Any

from datadog_api_client.v1.api.hosts_api import HostsApi
from datadog_api_client.v1.api.tags_api import TagsApi
from datadog_api_client.exceptions import ApiException

from ..client import get_api_client
from ..errors import sanitize_error


def _hosts_api() -> HostsApi:
    return HostsApi(get_api_client())


def _tags_api() -> TagsApi:
    return TagsApi(get_api_client())


def list_hosts(
    filter: str | None = None,
    sort_field: str | None = None,
    sort_dir: str | None = None,
    start: int | None = None,
    count: int | None = None,
    include_muted_hosts_data: bool | None = None,
    include_hosts_metadata: bool | None = None,
) -> str:
    """List hosts. GET /api/v1/hosts. Optional: filter, sort_field, sort_dir, start, count."""
    try:
        api = _hosts_api()
        resp = api.list_hosts(
            filter=filter,
            sort_field=sort_field,
            sort_dir=sort_dir,
            start=start,
            count=count,
            include_muted_hosts_data=include_muted_hosts_data,
            include_hosts_metadata=include_hosts_metadata,
        )
        return json.dumps(_host_list_response_to_dict(resp))
    except ApiException as e:
        return json.dumps({"error": sanitize_error(e)})


def get_host_tags(host_name: str, source: str | None = None) -> str:
    """Get tags for a host. GET /api/v1/tags/hosts/{host_name}."""
    try:
        api = _tags_api()
        resp = api.get_host_tags(host_name, source=source)
        return json.dumps(_host_tags_to_dict(resp))
    except ApiException as e:
        return json.dumps({"error": sanitize_error(e)})


def _host_list_response_to_dict(r: Any) -> dict:
    if hasattr(r, "to_dict"):
        return r.to_dict()
    return {"host_list": getattr(r, "host_list", []), "total_matching": getattr(r, "total_matching", None)}


def _host_tags_to_dict(r: Any) -> dict:
    if hasattr(r, "to_dict"):
        return r.to_dict()
    return {"tags": getattr(r, "tags", [])}
