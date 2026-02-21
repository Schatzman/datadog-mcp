"""
URI-addressable resources: datadog://monitors, datadog://dashboards, etc.
"""

import json

from .tools import dashboards, monitors


def get_monitors_list() -> str:
    """Fetch list of monitors (live)."""
    return monitors.list_monitors()


def get_monitor_by_id(monitor_id: str) -> str:
    """Fetch a single monitor by ID (live)."""
    return monitors.get_monitor(int(monitor_id))


def get_dashboards_list() -> str:
    """Fetch list of dashboards (live)."""
    return dashboards.list_dashboards()


def get_dashboard_by_id(dashboard_id: str) -> str:
    """Fetch a single dashboard by ID (live)."""
    return dashboards.get_dashboard(dashboard_id)
