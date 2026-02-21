"""
Incidents API (v2). DataDog API: https://docs.datadoghq.com/api/latest/incidents/
Scopes: incident_read, incident_write.
"""

import json
from typing import Any

from datadog_api_client.v2.api.incidents_api import IncidentsApi
from datadog_api_client.v2.model.incident_create_request import IncidentCreateRequest
from datadog_api_client.v2.model.incident_create_data import IncidentCreateData
from datadog_api_client.v2.model.incident_type import IncidentType
from datadog_api_client.v2.model.incident_update_request import IncidentUpdateRequest
from datadog_api_client.v2.model.incident_update_data import IncidentUpdateData
from datadog_api_client.v2.model.incident_create_attributes import IncidentCreateAttributes
from datadog_api_client.v2.model.incident_update_attributes import IncidentUpdateAttributes
from datadog_api_client.exceptions import ApiException

from ..client import get_api_client
from ..errors import sanitize_error


def _api() -> IncidentsApi:
    return IncidentsApi(get_api_client())


def list_incidents(
    page_size: int | None = None,
    page_offset: int | None = None,
) -> str:
    """List incidents. GET /api/v2/incidents."""
    try:
        api = _api()
        resp = api.list_incidents(page_size=page_size, page_offset=page_offset)
        return json.dumps(_incidents_response_to_dict(resp))
    except ApiException as e:
        return json.dumps({"error": sanitize_error(e)})


def get_incident(incident_id: str) -> str:
    """Get a single incident by ID. GET /api/v2/incidents/{incident_id}."""
    try:
        api = _api()
        resp = api.get_incident(incident_id)
        return json.dumps(_incident_response_to_dict(resp))
    except ApiException as e:
        return json.dumps({"error": sanitize_error(e)})


def create_incident(title: str, customer_impacted: bool = False) -> str:
    """Create an incident. POST /api/v2/incidents. Scope: incident_write."""
    try:
        api = _api()
        attrs = IncidentCreateAttributes(title=title, customer_impacted=customer_impacted)
        create_data = IncidentCreateData(type=IncidentType.INCIDENTS, attributes=attrs)
        req = IncidentCreateRequest(data=create_data)
        resp = api.create_incident(body=req)
        return json.dumps(_incident_response_to_dict(resp))
    except json.JSONDecodeError as e:
        return json.dumps({"error": f"Invalid JSON: {e!s}"})
    except (TypeError, ValueError) as e:
        return json.dumps({"error": str(e)})
    except ApiException as e:
        return json.dumps({"error": sanitize_error(e)})


def update_incident(incident_id: str, body_json: str) -> str:
    """Update an incident. PATCH /api/v2/incidents/{incident_id}. body_json: JSON object with attributes (e.g. title, customer_impacted). Scope: incident_write."""
    try:
        api = _api()
        attrs_dict = json.loads(body_json)
        if not isinstance(attrs_dict, dict):
            return json.dumps({"error": "body_json must be a JSON object"})
        attrs = IncidentUpdateAttributes(**attrs_dict)
        update_data = IncidentUpdateData(attributes=attrs)
        req = IncidentUpdateRequest(data=update_data)
        resp = api.update_incident(incident_id, body=req)
        return json.dumps(_incident_response_to_dict(resp))
    except json.JSONDecodeError as e:
        return json.dumps({"error": f"Invalid JSON: {e!s}"})
    except (TypeError, ValueError) as e:
        return json.dumps({"error": str(e)})
    except ApiException as e:
        return json.dumps({"error": sanitize_error(e)})


def _incidents_response_to_dict(r: Any) -> dict:
    if hasattr(r, "to_dict"):
        return r.to_dict()
    return {"data": getattr(r, "data", [])}


def _incident_response_to_dict(r: Any) -> dict:
    if hasattr(r, "to_dict"):
        return r.to_dict()
    return {}
