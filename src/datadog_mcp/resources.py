"""
URI-addressable resources: datadog://monitors, datadog://dashboards, datadog://downtimes, etc.
"""

from .tools import dashboards, downtimes, incidents, monitors, slos


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


def get_downtimes_list() -> str:
    """Fetch list of downtimes (live)."""
    return downtimes.list_downtimes()


def get_downtime_by_id(downtime_id: str) -> str:
    """Fetch a single downtime by ID (live)."""
    return downtimes.get_downtime(int(downtime_id))


def get_slos_list() -> str:
    """Fetch list of SLOs (live)."""
    return slos.list_slos()


def get_slo_by_id(slo_id: str) -> str:
    """Fetch a single SLO by ID (live)."""
    return slos.get_slo(slo_id)


def get_incidents_list() -> str:
    """Fetch list of incidents (live)."""
    return incidents.list_incidents()


def get_incident_by_id(incident_id: str) -> str:
    """Fetch a single incident by ID (live)."""
    return incidents.get_incident(incident_id)
