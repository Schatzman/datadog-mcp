"""
Synthetics API (v1). DataDog API: https://docs.datadoghq.com/api/latest/synthetics/
Scopes: synthetics_read.
"""

import json
from typing import Any

from datadog_api_client.v1.api.synthetics_api import SyntheticsApi
from datadog_api_client.exceptions import ApiException

from ..client import get_api_client
from ..errors import sanitize_error


def _api() -> SyntheticsApi:
    return SyntheticsApi(get_api_client())


def _to_dict(obj: Any) -> dict:
    """Convert API response to dict for JSON serialization."""
    if hasattr(obj, "to_dict"):
        return obj.to_dict()
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    return {"data": getattr(obj, "data", [])}


def list_synthetics_tests(
    page_size: int | None = None,
    page_number: int | None = None,
) -> str:
    """List Synthetic tests. GET list endpoint. Optional: page_size, page_number. Scope: synthetics_read."""
    try:
        api = _api()
        kwargs = {}
        if page_size is not None:
            kwargs["page_size"] = page_size
        if page_number is not None:
            kwargs["page_number"] = page_number
        resp = api.list_tests(**kwargs)
        return json.dumps(_to_dict(resp))
    except ApiException as e:
        return json.dumps({"error": sanitize_error(e)})


def get_synthetics_test(public_id: str) -> str:
    """Get a single Synthetic test by public_id. GET test by public_id. Scope: synthetics_read."""
    try:
        api = _api()
        resp = api.get_test(public_id=public_id)
        return json.dumps(_to_dict(resp))
    except ApiException as e:
        return json.dumps({"error": sanitize_error(e)})
