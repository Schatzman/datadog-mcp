# Tool reference

Per-tool parameters, scopes, and response shape. API details: [DataDog API Reference](https://docs.datadoghq.com/api/latest/). All tools return JSON strings; on failure they return `{"error": "..."}`.

## Rate limits (429)

On 429, the server retries with backoff (up to 2 retries). If still rate-limited, it returns a sanitized error. See [Rate Limits](https://docs.datadoghq.com/api/latest/rate-limits/).

---

## Authentication

### validate_keys_tool

- **Description:** Validate DataDog API and Application keys (GET /api/v1/validate).
- **Parameters:** None.
- **Scopes:** None (API key only).
- **Returns:** JSON with `valid` (bool) and optional `error` (string).
- **API:** [Authentication](https://docs.datadoghq.com/api/latest/authentication/)

---

## Monitors

[Monitors API](https://docs.datadoghq.com/api/latest/monitors/)

| Tool | Parameters | Scopes | Returns |
|------|------------|--------|---------|
| list_monitors | group_states, name, tags, monitor_tags, with_downtimes, page, page_size (all optional) | monitors_read | JSON array of monitor objects |
| get_monitor | monitor_id (int), with_downtimes (bool, default false) | monitors_read | Single monitor object |
| create_monitor | body_json (string): JSON with type, query, name, message, etc. | monitors_write | Created monitor object |
| update_monitor | monitor_id (int), body_json (string): optional name, message, query, options, tags | monitors_write | Updated monitor object |
| delete_monitor | monitor_id (int) | monitors_write | `{"ok": true, "deleted_monitor_id": id}` or error |
| mute_monitor | monitor_id (int) | monitors_write | `{"ok": true, "monitor_id": ..., "message": "Monitor muted."}` or error |
| unmute_monitor | monitor_id (int) | monitors_write | `{"ok": true, "monitor_id": ..., "message": "Monitor unmuted."}` or error |

---

## Dashboards

[Dashboards API](https://docs.datadoghq.com/api/latest/dashboards/)

| Tool | Parameters | Scopes | Returns |
|------|------------|--------|---------|
| list_dashboards | filter_shared, filter_deleted, count, start (all optional) | dashboards_read | JSON array of dashboard summary objects |
| get_dashboard | dashboard_id (str) | dashboards_read | Single dashboard object |
| create_dashboard | body_json: title, widgets, layout_type | dashboards_write | Created dashboard object |
| update_dashboard | dashboard_id, body_json | dashboards_write | Updated dashboard object |
| delete_dashboard | dashboard_id | dashboards_write | Deletion result or error |

---

## Metrics

[Metrics API](https://docs.datadoghq.com/api/v1/metrics/)

| Tool | Parameters | Scopes | Returns |
|------|------------|--------|---------|
| query_metrics | from_ts (int), to_ts (int), query (str) — Unix seconds and metric query | metrics_read | Query result JSON |

---

## Logs

[Logs API](https://docs.datadoghq.com/api/v1/logs/)

| Tool | Parameters | Scopes | Returns |
|------|------------|--------|---------|
| list_log_indexes | None | logs_read_config | List of index configs |
| query_logs | start_ts, end_ts (int), query (optional), limit (default 50), sort (default "desc"), index (optional) | logs_read | Log entries JSON |

---

## Events

[Events API](https://docs.datadoghq.com/api/v1/events/)

| Tool | Parameters | Scopes | Returns |
|------|------------|--------|---------|
| list_events | start_ts, end_ts (int), priority, sources, tags, page (optional) | events_read | Events list JSON |

---

## Hosts

[Hosts API](https://docs.datadoghq.com/api/v1/hosts/)

| Tool | Parameters | Scopes | Returns |
|------|------------|--------|---------|
| list_hosts | filter, sort_field, sort_dir, start, count, include_muted_hosts_data, include_hosts_metadata (optional) | infrastructure_read | Hosts list |
| get_host_tags | host_name (str), source (optional) | tags_read | Tags for the host |

---

## Service Level Objectives

[SLOs API](https://docs.datadoghq.com/api/v1/service-level-objectives/)

| Tool | Parameters | Scopes | Returns |
|------|------------|--------|---------|
| list_slos | ids, query, tags_query, metrics_query, limit, offset (optional) | slo_read | SLO list |
| get_slo | slo_id (str), with_configured_alert_ids (bool, default false) | slo_read | Single SLO object |

---

## Downtimes (v1)

[Downtimes API](https://docs.datadoghq.com/api/latest/downtimes/)

| Tool | Parameters | Scopes | Returns |
|------|------------|--------|---------|
| list_downtimes | current_only, with_creator (optional) | monitors_read | JSON array of downtime objects |
| get_downtime | downtime_id (int) | monitors_read | Single downtime object |
| create_downtime | body_json: scope (list), start (int), optional end, message, monitor_id | monitors_write | Created downtime object |
| update_downtime | downtime_id (int), body_json | monitors_write | Updated downtime object |
| cancel_downtime | downtime_id (int) | monitors_write | `{"ok": true, "downtime_id": id, "message": "..."}` or error |

---

## Incidents (v2)

[Incidents API](https://docs.datadoghq.com/api/latest/incidents/)

| Tool | Parameters | Scopes | Returns |
|------|------------|--------|---------|
| list_incidents | page_size, page_offset (optional) | incident_read | Incidents list |
| get_incident | incident_id (str) | incident_read | Single incident object |
| create_incident | title (str), customer_impacted (bool, default false) | incident_write | Created incident |
| update_incident | incident_id, body_json (attributes) | incident_write | Updated incident |

---

## APM

[APM API](https://docs.datadoghq.com/api/latest/apm/)

| Tool | Parameters | Scopes | Returns |
|------|------------|--------|---------|
| list_apm_services | filter_env (str, default "*") | apm_read | APM services list |

---

## Synthetics

[Synthetics API](https://docs.datadoghq.com/api/latest/synthetics/)

| Tool | Parameters | Scopes | Returns |
|------|------------|--------|---------|
| list_synthetics_tests | page_size, page_number (optional) | synthetics_read | JSON list of Synthetic tests |
| get_synthetics_test | public_id (str) | synthetics_read | Single Synthetic test object |

---

## Notebooks

[Notebooks API](https://docs.datadoghq.com/api/latest/notebooks/)

| Tool | Parameters | Scopes | Returns |
|------|------------|--------|---------|
| list_notebooks | count, start (optional) | notebooks_read | JSON list of notebook summaries |
| get_notebook | notebook_id (str) | notebooks_read | Single notebook object |

---

## Usage

[Usage metering](https://docs.datadoghq.com/api/v1/usage-metering/)

| Tool | Parameters | Scopes | Returns |
|------|------------|--------|---------|
| get_usage_summary | start_month (YYYY-MM), end_month (optional), include_org_details (bool, default false) | usage_read | Usage summary JSON |

---

## Resources (URI)

Resources return the same JSON shape as the corresponding list/get tools:

- `datadog://validate` — validation result
- `datadog://monitors` — list of monitors
- `datadog://monitors/{id}` — single monitor
- `datadog://dashboards` — list of dashboards
- `datadog://dashboards/{id}` — single dashboard
- `datadog://downtimes` — list of downtimes
- `datadog://downtimes/{id}` — single downtime
- `datadog://slos` — list of SLOs
- `datadog://slos/{id}` — single SLO
- `datadog://incidents` — list of incidents
- `datadog://incidents/{id}` — single incident

## Prompts

Prompts build a string for the LLM using tool data; they do not call the API directly.

| Prompt | Parameters | Uses data from |
|--------|------------|----------------|
| prompt_summarize_monitor_state | monitor_id | get_monitor |
| prompt_draft_incident_status | incident_id | get_incident |
| prompt_summarize_slo | slo_id | get_slo |
| prompt_dashboard_insights | dashboard_id | get_dashboard |
