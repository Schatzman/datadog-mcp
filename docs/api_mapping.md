# DataDog API → MCP mapping (evidence)

This document maps each MCP tool and resource to the official DataDog API endpoint and scopes. Use it to audit behavior and required permissions.

References:

- [DataDog API Reference](https://docs.datadoghq.com/api/latest/)
- [Using the API](https://docs.datadoghq.com/api/latest/using-the-api/)
- [Authorization Scopes](https://docs.datadoghq.com/api/latest/scopes/)
- [Rate Limits](https://docs.datadoghq.com/api/latest/rate-limits/)

## Authentication

| MCP tool / resource   | DataDog endpoint        | Scopes  |
|-----------------------|-------------------------|--------|
| `validate_keys_tool`  | GET /api/v1/validate    | (API key only) |
| `datadog://validate`  | GET /api/v1/validate    | (API key only) |

## Monitors

| MCP tool / resource   | DataDog endpoint              | Scopes         |
|-----------------------|------------------------------|----------------|
| `list_monitors`       | GET /api/v1/monitor          | monitors_read  |
| `get_monitor`         | GET /api/v1/monitor/{id}     | monitors_read  |
| `create_monitor`      | POST /api/v1/monitor         | monitors_write |
| `mute_monitor`        | PATCH /api/v1/monitor/{id}   | monitors_write |
| `unmute_monitor`      | PATCH /api/v1/monitor/{id}   | monitors_write |
| `update_monitor`      | PATCH /api/v1/monitor/{id}   | monitors_write |
| `delete_monitor`       | DELETE /api/v1/monitor/{id}  | monitors_write |
| `datadog://monitors`   | GET /api/v1/monitor          | monitors_read  |
| `datadog://monitors/{id}` | GET /api/v1/monitor/{id} | monitors_read  |

## Dashboards

| MCP tool / resource      | DataDog endpoint                | Scopes          |
|--------------------------|---------------------------------|-----------------|
| `list_dashboards`       | GET /api/v1/dashboard           | dashboards_read |
| `get_dashboard`         | GET /api/v1/dashboard/{id}      | dashboards_read |
| `create_dashboard`      | POST /api/v1/dashboard          | dashboards_write|
| `update_dashboard`      | PUT /api/v1/dashboard/{id}      | dashboards_write|
| `delete_dashboard`      | DELETE /api/v1/dashboard/{id}   | dashboards_write|
| `datadog://dashboards`   | GET /api/v1/dashboard           | dashboards_read |
| `datadog://dashboards/{id}` | GET /api/v1/dashboard/{id}  | dashboards_read |

## Metrics

| MCP tool    | DataDog endpoint   | Scopes      |
|-------------|--------------------|-------------|
| `query_metrics` | GET /api/v1/query | metrics_read |

## Logs

| MCP tool           | DataDog endpoint              | Scopes           |
|--------------------|-------------------------------|------------------|
| `list_log_indexes` | GET /api/v1/logs/config/indexes | logs_read_config |
| `query_logs`       | POST /api/v1/logs-queries/list | logs_read        |

## Events

| MCP tool      | DataDog endpoint    | Scopes     |
|---------------|---------------------|------------|
| `list_events` | GET /api/v1/events  | events_read|

## Hosts

| MCP tool        | DataDog endpoint        | Scopes             |
|-----------------|-------------------------|--------------------|
| `list_hosts`    | GET /api/v1/hosts       | infrastructure_read|
| `get_host_tags` | GET /api/v1/tags/hosts/{name} | tags_read   |

## Service Level Objectives

| MCP tool / resource | DataDog endpoint   | Scopes   |
|---------------------|--------------------|----------|
| `list_slos`         | GET /api/v1/slo     | slo_read |
| `get_slo`           | GET /api/v1/slo/{id}| slo_read |
| `datadog://slos`    | GET /api/v1/slo     | slo_read |
| `datadog://slos/{id}` | GET /api/v1/slo/{id}| slo_read |

## Incidents (v2)

| MCP tool / resource   | DataDog endpoint           | Scopes        |
|-----------------------|----------------------------|---------------|
| `list_incidents`     | GET /api/v2/incidents      | incident_read |
| `get_incident`       | GET /api/v2/incidents/{id} | incident_read |
| `create_incident`    | POST /api/v2/incidents     | incident_write|
| `update_incident`    | PATCH /api/v2/incidents/{id}| incident_write|
| `datadog://incidents`| GET /api/v2/incidents      | incident_read |
| `datadog://incidents/{id}` | GET /api/v2/incidents/{id} | incident_read |

## APM

| MCP tool            | DataDog endpoint      | Scopes   |
|---------------------|-----------------------|----------|
| `list_apm_services` | GET /api/v2/apm/services | apm_read |

## Synthetics

| MCP tool                 | DataDog endpoint                    | Scopes          |
|-------------------------|-------------------------------------|-----------------|
| `list_synthetics_tests` | GET /api/v1/synthetics/tests (list)  | synthetics_read |
| `get_synthetics_test`   | GET /api/v1/synthetics/tests/{public_id} | synthetics_read |

## Notebooks

| MCP tool           | DataDog endpoint                  | Scopes         |
|--------------------|-----------------------------------|----------------|
| `list_notebooks`   | GET /api/v1/notebooks (list)      | notebooks_read |
| `get_notebook`     | GET /api/v1/notebooks/{notebook_id} | notebooks_read |

## Downtimes (v1)

| MCP tool / resource    | DataDog endpoint               | Scopes          |
|------------------------|--------------------------------|------------------|
| `list_downtimes`       | GET /api/v1/downtime           | monitors_read    |
| `get_downtime`         | GET /api/v1/downtime/{id}      | monitors_read    |
| `create_downtime`      | POST /api/v1/downtime          | monitors_write   |
| `update_downtime`      | PATCH /api/v1/downtime/{id}    | monitors_write   |
| `cancel_downtime`      | DELETE /api/v1/downtime/{id}   | monitors_write   |
| `datadog://downtimes`  | GET /api/v1/downtime           | monitors_read   |
| `datadog://downtimes/{id}` | GET /api/v1/downtime/{id}  | monitors_read   |

## Usage

| MCP tool           | DataDog endpoint        | Scopes    |
|--------------------|-------------------------|-----------|
| `get_usage_summary`| GET /api/v1/usage/summary| usage_read|

## Prompts

Prompts do not call the API directly; they use tool/resource data to build a prompt string for the LLM:

| MCP prompt                     | Uses data from        |
|--------------------------------|------------------------|
| `prompt_summarize_monitor_state` | `get_monitor` (by ID) |
| `prompt_draft_incident_status`   | `get_incident` (by ID)|
| `prompt_summarize_slo`           | `get_slo` (by ID)     |
| `prompt_dashboard_insights`      | `get_dashboard` (by ID)|
