# DataDog MCP Server

Evidence-driven MCP server that exposes DataDog as **tools**, **resources**, and **prompts**. Uses the official [DataDog API](https://docs.datadoghq.com/api/latest/) and [MCP Python SDK](https://modelcontextprotocol.github.io/python-sdk/).

## Requirements

- Python 3.10+
- DataDog API key and Application key ([create here](https://app.datadoghq.com/organization-settings/api-keys))

## Quick start

1. Clone or enter this repo, then install: `uv sync`
2. Copy `.env.example` to `.env` and set `DD_API_KEY` and `DD_APP_KEY` (create keys at [DataDog API keys](https://app.datadoghq.com/organization-settings/api-keys)). Never commit `.env`.
3. Run the server: `uv run python -m datadog_mcp.server` (stdio) or use streamable HTTP (see below).

## Configuration

Set credentials via environment variables (do **not** commit real values):

| Variable      | Required | Description                    |
|---------------|----------|--------------------------------|
| `DD_API_KEY`  | Yes      | DataDog API key                |
| `DD_APP_KEY`  | Yes      | DataDog Application key       |
| `DD_SITE`     | No       | Site (default: `datadoghq.com`; use `datadoghq.eu`, `ap1.datadoghq.com`, etc.) |

Copy `.env.example` to `.env` and fill in values locally; never commit `.env`.

## Cursor / MCP client setup

To attach this server as an MCP in Cursor (or another stdio client):

- **Command:** `uv run python -m datadog_mcp.server` (run from the `datadog-mcp` directory).
- **Env:** Ensure `DD_API_KEY` and `DD_APP_KEY` are set in the environment where the client runs (e.g. in Cursor’s MCP settings or your shell).

Example MCP config snippet (path and env depend on your setup):

```json
{
  "mcpServers": {
    "datadog": {
      "command": "uv",
      "args": ["run", "python", "-m", "datadog_mcp.server"],
      "cwd": "/path/to/datadog-mcp",
      "env": { "DD_API_KEY": "<your-api-key>", "DD_APP_KEY": "<your-app-key>" }
    }
  }
}
```

## Running the server

**Default: stdio** (for Cursor, CLI clients):

```bash
cd datadog-mcp
uv run python -m datadog_mcp.server
# or with explicit stdio:
uv run python -m datadog_mcp.server stdio
```

**Streamable HTTP** (for [MCP Inspector](https://github.com/modelcontextprotocol/inspector), browser-based clients):

```bash
uv run python -c "from datadog_mcp.server import run; run(transport='streamable-http')"
```

Then connect the MCP Inspector to the shown URL (e.g. `http://localhost:8000/mcp`).

## Tools

| Tool | Description | Scope |
|------|-------------|--------|
| `validate_keys_tool` | Validate API/Application keys | — |
| `list_monitors`, `get_monitor`, `create_monitor`, `update_monitor`, `delete_monitor`, `mute_monitor`, `unmute_monitor` | Monitors | monitors_read, monitors_write |
| `list_dashboards`, `get_dashboard`, `create_dashboard`, `update_dashboard`, `delete_dashboard` | Dashboards | dashboards_read, dashboards_write |
| `query_metrics` | Metrics query | metrics_read |
| `list_log_indexes`, `query_logs` | Logs | logs_read_config, logs_read |
| `list_events` | Events | events_read |
| `list_hosts`, `get_host_tags` | Hosts / tags | infrastructure_read, tags_read |
| `list_slos`, `get_slo` | SLOs | slo_read |
| `list_downtimes`, `get_downtime`, `create_downtime`, `update_downtime`, `cancel_downtime` | Downtimes (v1) | monitors_read, monitors_write |
| `list_incidents`, `get_incident`, `create_incident`, `update_incident` | Incidents (v2) | incident_read, incident_write |
| `list_apm_services` | APM services | apm_read |
| `list_synthetics_tests`, `get_synthetics_test` | Synthetics | synthetics_read |
| `list_notebooks`, `get_notebook` | Notebooks | notebooks_read |
| `get_usage_summary` | Usage metering | usage_read |

## Resources (URI)

- `datadog://validate` — API key validation status
- `datadog://monitors` — List of monitors
- `datadog://monitors/{id}` — Single monitor by ID
- `datadog://dashboards` — List of dashboards
- `datadog://dashboards/{id}` — Single dashboard by ID
- `datadog://downtimes` — List of downtimes
- `datadog://downtimes/{id}` — Single downtime by ID
- `datadog://slos` — List of SLOs
- `datadog://slos/{id}` — Single SLO by ID
- `datadog://incidents` — List of incidents
- `datadog://incidents/{id}` — Single incident by ID

## Prompts

- `prompt_summarize_monitor_state(monitor_id)` — Ask the LLM to summarize a monitor’s state
- `prompt_draft_incident_status(incident_id)` — Ask the LLM to draft a status message from an incident
- `prompt_summarize_slo(slo_id)` — Ask the LLM to summarize SLO state and burn rate
- `prompt_dashboard_insights(dashboard_id)` — Ask the LLM to summarize key widgets and suggest focus areas

Full endpoint → tool mapping and scopes: [docs/api_mapping.md](docs/api_mapping.md). For detailed tool parameters, scopes, and examples: [docs/tool_reference.md](docs/tool_reference.md).

## Development

```bash
uv sync
uv run pytest
```

## DataDog scopes and rate limits

- **Scopes:** See [Authorization Scopes](https://docs.datadoghq.com/api/latest/scopes/). Each tool documents the scope it needs; grant the minimum required.
- **Rate limits:** See [Rate Limits](https://docs.datadoghq.com/api/latest/rate-limits/). On 429 the server retries with backoff (see docs/tool_reference.md); if still rate-limited, it returns a sanitized error.

## Secrets

Do **not** log, echo, or commit `DD_API_KEY` or `DD_APP_KEY`. Use environment variables or a secure secret manager only.
