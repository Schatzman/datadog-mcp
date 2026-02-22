"""
DataDog MCP server: FastMCP app with tools, resources, and prompts.
Default transport: stdio. Use transport="streamable-http" for MCP Inspector.
"""

import json

from mcp.server.fastmcp import FastMCP

from .client import validate_keys
from .resources import (
    get_dashboard_by_id,
    get_dashboards_list,
    get_downtime_by_id,
    get_downtimes_list,
    get_incident_by_id,
    get_incidents_list,
    get_monitor_by_id,
    get_monitors_list,
    get_slo_by_id,
    get_slos_list,
)
from .tools import apm, dashboards, downtimes, events, hosts, incidents, logs, metrics, monitors, slos, synthetics, usage

mcp = FastMCP(
    "DataDog MCP",
    json_response=True,
)


@mcp.tool()
def validate_keys_tool() -> str:
    """
    Validate DataDog API and Application keys (GET /api/v1/validate).
    Returns whether the current credentials are valid.
    Required scopes: none (API key only).
    See: https://docs.datadoghq.com/api/latest/authentication/
    """
    result = validate_keys()
    return json.dumps(result)


# --- Monitors (https://docs.datadoghq.com/api/latest/monitors/) ---
@mcp.tool()
def list_monitors(
    group_states: str | None = None,
    name: str | None = None,
    tags: str | None = None,
    monitor_tags: str | None = None,
    with_downtimes: bool | None = None,
    page: int | None = None,
    page_size: int | None = None,
) -> str:
    """List monitors. Optional: group_states, name, tags, monitor_tags, with_downtimes, page, page_size. Scope: monitors_read."""
    return monitors.list_monitors(
        group_states=group_states,
        name=name,
        tags=tags,
        monitor_tags=monitor_tags,
        with_downtimes=with_downtimes,
        page=page,
        page_size=page_size,
    )


@mcp.tool()
def get_monitor(monitor_id: int, with_downtimes: bool = False) -> str:
    """Get a single monitor by ID. Scope: monitors_read."""
    return monitors.get_monitor(monitor_id, with_downtimes=with_downtimes)


@mcp.tool()
def create_monitor(body_json: str) -> str:
    """Create a monitor. body_json: JSON with type, query, name, message. Scope: monitors_write."""
    return monitors.create_monitor(body_json)


@mcp.tool()
def mute_monitor(monitor_id: int) -> str:
    """Mute a monitor. Scope: monitors_write."""
    return monitors.mute_monitor(monitor_id)


@mcp.tool()
def unmute_monitor(monitor_id: int) -> str:
    """Unmute a monitor. Scope: monitors_write."""
    return monitors.unmute_monitor(monitor_id)


@mcp.tool()
def update_monitor(monitor_id: int, body_json: str) -> str:
    """Update a monitor. body_json: JSON with optional name, message, query, options, tags. Scope: monitors_write. Returns: updated monitor object or error."""
    return monitors.update_monitor(monitor_id, body_json)


@mcp.tool()
def delete_monitor(monitor_id: int) -> str:
    """Delete a monitor. Scope: monitors_write. Returns: {\"ok\": true, \"deleted_monitor_id\": id} or error."""
    return monitors.delete_monitor(monitor_id)


# --- Downtimes (https://docs.datadoghq.com/api/latest/downtimes/) ---
@mcp.tool()
def list_downtimes(current_only: bool | None = None, with_creator: bool | None = None) -> str:
    """List downtimes. Optional: current_only, with_creator. Scope: monitors_read."""
    return downtimes.list_downtimes(current_only=current_only, with_creator=with_creator)


@mcp.tool()
def get_downtime(downtime_id: int) -> str:
    """Get a single downtime by ID. Scope: monitors_read."""
    return downtimes.get_downtime(downtime_id)


@mcp.tool()
def create_downtime(body_json: str) -> str:
    """Create a downtime. body_json: JSON with scope (list), start (Unix ts), optional end, message. Scope: monitors_write."""
    return downtimes.create_downtime(body_json)


@mcp.tool()
def update_downtime(downtime_id: int, body_json: str) -> str:
    """Update a downtime. body_json: JSON with optional scope, start, end, message. Scope: monitors_write."""
    return downtimes.update_downtime(downtime_id, body_json)


@mcp.tool()
def cancel_downtime(downtime_id: int) -> str:
    """Cancel a downtime. Scope: monitors_write."""
    return downtimes.cancel_downtime(downtime_id)


# --- Dashboards (https://docs.datadoghq.com/api/latest/dashboards/) ---
@mcp.tool()
def list_dashboards(
    filter_shared: bool | None = None,
    filter_deleted: bool | None = None,
    count: int | None = None,
    start: int | None = None,
) -> str:
    """List dashboards. Optional: filter_shared, filter_deleted, count, start. Scope: dashboards_read."""
    return dashboards.list_dashboards(
        filter_shared=filter_shared,
        filter_deleted=filter_deleted,
        count=count,
        start=start,
    )


@mcp.tool()
def get_dashboard(dashboard_id: str) -> str:
    """Get a single dashboard by ID. Scope: dashboards_read."""
    return dashboards.get_dashboard(dashboard_id)


@mcp.tool()
def create_dashboard(body_json: str) -> str:
    """Create a dashboard. body_json: JSON with title, widgets, layout_type. Scope: dashboards_write."""
    return dashboards.create_dashboard(body_json)


@mcp.tool()
def update_dashboard(dashboard_id: str, body_json: str) -> str:
    """Update a dashboard. Scope: dashboards_write."""
    return dashboards.update_dashboard(dashboard_id, body_json)


@mcp.tool()
def delete_dashboard(dashboard_id: str) -> str:
    """Delete a dashboard. Scope: dashboards_write."""
    return dashboards.delete_dashboard(dashboard_id)


# --- Metrics (https://docs.datadoghq.com/api/v1/metrics/) ---
@mcp.tool()
def query_metrics(from_ts: int, to_ts: int, query: str) -> str:
    """Query metrics in a time range. from_ts and to_ts are Unix seconds. Scope: metrics_read."""
    return metrics.query_metrics(from_ts=from_ts, to_ts=to_ts, query=query)


# --- Logs (https://docs.datadoghq.com/api/v1/logs/) ---
@mcp.tool()
def list_log_indexes() -> str:
    """List log indexes. Scope: logs_read_config."""
    return logs.list_log_indexes()


@mcp.tool()
def query_logs(
    start_ts: int,
    end_ts: int,
    query: str | None = None,
    limit: int = 50,
    sort: str = "desc",
    index: str | None = None,
) -> str:
    """Query logs in a time range. start_ts/end_ts in Unix seconds. Scope: logs_read."""
    return logs.query_logs(
        start_ts=start_ts,
        end_ts=end_ts,
        query=query,
        limit=limit,
        sort=sort,
        index=index,
    )


# --- Events (https://docs.datadoghq.com/api/v1/events/) ---
@mcp.tool()
def list_events(
    start_ts: int,
    end_ts: int,
    priority: str | None = None,
    sources: str | None = None,
    tags: str | None = None,
    page: int | None = None,
) -> str:
    """List events in a time range. start_ts/end_ts in Unix seconds. Scope: events_read."""
    return events.list_events(
        start_ts=start_ts,
        end_ts=end_ts,
        priority=priority,
        sources=sources,
        tags=tags,
        page=page,
    )


# --- Hosts (https://docs.datadoghq.com/api/v1/hosts/) ---
@mcp.tool()
def list_hosts(
    filter: str | None = None,
    sort_field: str | None = None,
    sort_dir: str | None = None,
    start: int | None = None,
    count: int | None = None,
    include_muted_hosts_data: bool | None = None,
    include_hosts_metadata: bool | None = None,
) -> str:
    """List hosts. Optional: filter, sort_field, sort_dir, start, count. Scope: infrastructure_read."""
    return hosts.list_hosts(
        filter=filter,
        sort_field=sort_field,
        sort_dir=sort_dir,
        start=start,
        count=count,
        include_muted_hosts_data=include_muted_hosts_data,
        include_hosts_metadata=include_hosts_metadata,
    )


@mcp.tool()
def get_host_tags(host_name: str, source: str | None = None) -> str:
    """Get tags for a host. Scope: tags_read."""
    return hosts.get_host_tags(host_name, source=source)


# --- SLOs (https://docs.datadoghq.com/api/v1/service-level-objectives/) ---
@mcp.tool()
def list_slos(
    ids: str | None = None,
    query: str | None = None,
    tags_query: str | None = None,
    metrics_query: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
) -> str:
    """List SLOs. Scope: slo_read."""
    return slos.list_slos(ids=ids, query=query, tags_query=tags_query, metrics_query=metrics_query, limit=limit, offset=offset)


@mcp.tool()
def get_slo(slo_id: str, with_configured_alert_ids: bool = False) -> str:
    """Get a single SLO by ID. Scope: slo_read."""
    return slos.get_slo(slo_id, with_configured_alert_ids=with_configured_alert_ids)


# --- Incidents v2 (https://docs.datadoghq.com/api/latest/incidents/) ---
@mcp.tool()
def list_incidents(page_size: int | None = None, page_offset: int | None = None) -> str:
    """List incidents. Scope: incident_read."""
    return incidents.list_incidents(page_size=page_size, page_offset=page_offset)


@mcp.tool()
def get_incident(incident_id: str) -> str:
    """Get a single incident by ID. Scope: incident_read."""
    return incidents.get_incident(incident_id)


@mcp.tool()
def create_incident(title: str, customer_impacted: bool = False) -> str:
    """Create an incident. Scope: incident_write."""
    return incidents.create_incident(title=title, customer_impacted=customer_impacted)


@mcp.tool()
def update_incident(incident_id: str, body_json: str) -> str:
    """Update an incident. body_json: JSON with attributes (e.g. title, customer_impacted). Scope: incident_write."""
    return incidents.update_incident(incident_id, body_json)


# --- APM (https://docs.datadoghq.com/api/latest/apm/) ---
@mcp.tool()
def list_apm_services(filter_env: str = "*") -> str:
    """List APM services. filter_env: environment, use '*' for all. Scope: apm_read."""
    return apm.list_apm_services(filter_env=filter_env)


# --- Synthetics (https://docs.datadoghq.com/api/latest/synthetics/) ---
@mcp.tool()
def list_synthetics_tests(page_size: int | None = None, page_number: int | None = None) -> str:
    """List Synthetic tests. Optional: page_size, page_number. Scope: synthetics_read."""
    return synthetics.list_synthetics_tests(page_size=page_size, page_number=page_number)


@mcp.tool()
def get_synthetics_test(public_id: str) -> str:
    """Get a single Synthetic test by public_id. Scope: synthetics_read."""
    return synthetics.get_synthetics_test(public_id=public_id)


# --- Usage (https://docs.datadoghq.com/api/v1/usage-metering/) ---
@mcp.tool()
def get_usage_summary(start_month: str, end_month: str | None = None, include_org_details: bool = False) -> str:
    """Get usage summary. start_month/end_month: YYYY-MM. Scope: usage_read."""
    return usage.get_usage_summary(start_month=start_month, end_month=end_month, include_org_details=include_org_details)


@mcp.resource("datadog://validate")
def resource_validate() -> str:
    """DataDog API key validation status (live)."""
    result = validate_keys()
    return json.dumps(result)


@mcp.resource("datadog://monitors")
def resource_monitors_list() -> str:
    """List of DataDog monitors (live)."""
    return get_monitors_list()


@mcp.resource("datadog://monitors/{monitor_id}")
def resource_monitor(monitor_id: str) -> str:
    """Single monitor JSON by ID (live)."""
    return get_monitor_by_id(monitor_id)


@mcp.resource("datadog://dashboards")
def resource_dashboards_list() -> str:
    """List of DataDog dashboards (live)."""
    return get_dashboards_list()


@mcp.resource("datadog://dashboards/{dashboard_id}")
def resource_dashboard(dashboard_id: str) -> str:
    """Single dashboard JSON by ID (live)."""
    return get_dashboard_by_id(dashboard_id)


@mcp.resource("datadog://downtimes")
def resource_downtimes_list() -> str:
    """List of DataDog downtimes (live)."""
    return get_downtimes_list()


@mcp.resource("datadog://downtimes/{downtime_id}")
def resource_downtime(downtime_id: str) -> str:
    """Single downtime JSON by ID (live)."""
    return get_downtime_by_id(downtime_id)


@mcp.resource("datadog://slos")
def resource_slos_list() -> str:
    """List of DataDog SLOs (live)."""
    return get_slos_list()


@mcp.resource("datadog://slos/{slo_id}")
def resource_slo(slo_id: str) -> str:
    """Single SLO JSON by ID (live)."""
    return get_slo_by_id(slo_id)


@mcp.resource("datadog://incidents")
def resource_incidents_list() -> str:
    """List of DataDog incidents (live)."""
    return get_incidents_list()


@mcp.resource("datadog://incidents/{incident_id}")
def resource_incident(incident_id: str) -> str:
    """Single incident JSON by ID (live)."""
    return get_incident_by_id(incident_id)


# --- Prompts ---
@mcp.prompt()
def prompt_summarize_monitor_state(monitor_id: str) -> str:
    """Generate a prompt asking the LLM to summarize the state of a monitor. Pass monitor_id."""
    raw = get_monitor_by_id(monitor_id)
    try:
        data = json.loads(raw)
        if "error" in data:
            return f"The monitor request failed: {data['error']}. Ask the user to check the monitor ID."
        return f"Summarize the following DataDog monitor state in 2–3 sentences for a status report. Focus on name, type, overall state, and any message.\n\nMonitor data:\n{json.dumps(data, indent=2)}"
    except json.JSONDecodeError:
        return f"Summarize the following DataDog monitor (raw):\n\n{raw}"


@mcp.prompt()
def prompt_draft_incident_status(incident_id: str) -> str:
    """Generate a prompt asking the LLM to draft a status message from an incident. Pass incident_id."""
    raw = incidents.get_incident(incident_id)
    try:
        data = json.loads(raw)
        if "error" in data:
            return f"The incident request failed: {data['error']}. Ask the user to check the incident ID."
        return f"Using the following DataDog incident, draft a short status message (1–2 paragraphs) suitable for internal or customer communication. Include current state and impact if present.\n\nIncident data:\n{json.dumps(data, indent=2)}"
    except json.JSONDecodeError:
        return f"Draft a status message from this incident (raw):\n\n{raw}"


@mcp.prompt()
def prompt_summarize_slo(slo_id: str) -> str:
    """Generate a prompt asking the LLM to summarize the SLO state and burn rate. Pass slo_id."""
    raw = get_slo_by_id(slo_id)
    try:
        data = json.loads(raw)
        if "error" in data:
            return f"The SLO request failed: {data['error']}. Ask the user to check the SLO ID."
        return f"Summarize the following DataDog SLO in 2–3 sentences for a status report. Include name, target, current state, error budget, and burn rate if present.\n\nSLO data:\n{json.dumps(data, indent=2)}"
    except json.JSONDecodeError:
        return f"Summarize the following DataDog SLO (raw):\n\n{raw}"


@mcp.prompt()
def prompt_dashboard_insights(dashboard_id: str) -> str:
    """Generate a prompt asking the LLM to summarize key widgets and suggest focus areas. Pass dashboard_id."""
    raw = get_dashboard_by_id(dashboard_id)
    try:
        data = json.loads(raw)
        if "error" in data:
            return f"The dashboard request failed: {data['error']}. Ask the user to check the dashboard ID."
        return f"Using the following DataDog dashboard, summarize the key widgets and metrics in 2–3 sentences, then suggest 1–2 focus areas or potential issues to investigate.\n\nDashboard data:\n{json.dumps(data, indent=2)}"
    except json.JSONDecodeError:
        return f"Summarize this dashboard and suggest focus areas (raw):\n\n{raw}"


def run(transport: str = "stdio") -> None:
    """Run the server. Default: stdio. Use 'streamable-http' for HTTP (e.g. MCP Inspector)."""
    mcp.run(transport=transport)


if __name__ == "__main__":
    import sys
    transport = sys.argv[1] if len(sys.argv) > 1 else "stdio"
    run(transport=transport)
