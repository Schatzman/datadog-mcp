"""
Usage Metering API. DataDog API: https://docs.datadoghq.com/api/v1/usage-metering/
Scopes: usage_read.
"""

import json
from datetime import datetime
from typing import Any

from datadog_api_client.v1.api.usage_metering_api import UsageMeteringApi
from datadog_api_client.exceptions import ApiException

from ..client import get_api_client
from ..errors import sanitize_error


def _api() -> UsageMeteringApi:
    return UsageMeteringApi(get_api_client())


def get_usage_summary(
    start_month: str,
    end_month: str | None = None,
    include_org_details: bool = False,
) -> str:
    """Get usage summary. GET /api/v1/usage/summary. start_month/end_month: YYYY-MM. Scope: usage_read."""
    try:
        api = _api()
        start_dt = datetime.strptime(start_month, "%Y-%m")
        end_dt = datetime.strptime(end_month, "%Y-%m") if end_month else None
        resp = api.get_usage_summary(
            start_month=start_dt,
            end_month=end_dt,
            include_org_details=include_org_details,
        )
        return json.dumps(_usage_summary_to_dict(resp))
    except ValueError as e:
        return json.dumps({"error": f"Invalid date format (use YYYY-MM): {e!s}"})
    except ApiException as e:
        return json.dumps({"error": sanitize_error(e)})


def _usage_summary_to_dict(r: Any) -> dict:
    if hasattr(r, "to_dict"):
        return r.to_dict()
    return {}
