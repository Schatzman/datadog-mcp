"""Test that the MCP server exposes expected tools, resources, and prompts."""

import asyncio

import pytest

from datadog_mcp.server import mcp


@pytest.mark.asyncio
async def test_server_exposes_expected_tools():
    """FastMCP app exposes key tools (allow-list)."""
    tools = await mcp.list_tools()
    names = {t.name for t in tools}
    expected = {
        "validate_keys_tool",
        "list_monitors",
        "get_monitor",
        "create_monitor",
        "update_monitor",
        "delete_monitor",
        "mute_monitor",
        "unmute_monitor",
        "list_downtimes",
        "get_downtime",
        "list_dashboards",
        "get_dashboard",
        "query_metrics",
        "list_slos",
        "get_slo",
        "list_incidents",
        "get_incident",
    }
    missing = expected - names
    assert not missing, f"Expected tools not registered: {missing}"


@pytest.mark.asyncio
async def test_server_exposes_expected_resources():
    """FastMCP app exposes key resource templates (parameterized URIs)."""
    templates = await mcp.list_resource_templates()
    uris = set()
    for t in templates:
        d = t.model_dump() if hasattr(t, "model_dump") else {}
        uri = d.get("uriTemplate") or d.get("uri_template")
        if uri:
            uris.add(uri)
    # list_resource_templates returns parameterized templates (with {id})
    expected = {
        "datadog://monitors/{monitor_id}",
        "datadog://dashboards/{dashboard_id}",
        "datadog://downtimes/{downtime_id}",
        "datadog://slos/{slo_id}",
        "datadog://incidents/{incident_id}",
    }
    missing = expected - uris
    assert not missing, f"Expected resources not registered: {missing}"


@pytest.mark.asyncio
async def test_server_exposes_expected_prompts():
    """FastMCP app exposes key prompts."""
    prompts = await mcp.list_prompts()
    names = {p.name for p in prompts}
    expected = {
        "prompt_summarize_monitor_state",
        "prompt_draft_incident_status",
        "prompt_summarize_slo",
        "prompt_dashboard_insights",
    }
    missing = expected - names
    assert not missing, f"Expected prompts not registered: {missing}"
