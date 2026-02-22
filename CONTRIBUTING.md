# Contributing to DataDog MCP

## Development setup

1. Install dependencies: `uv sync`
2. Copy `.env.example` to `.env` and set `DD_API_KEY` and `DD_APP_KEY` (never commit `.env`).
3. Run tests: `uv run pytest`

## Adding a new tool

1. **API mapping:** Add the tool and its DataDog endpoint and scopes to [docs/api_mapping.md](docs/api_mapping.md).
2. **Implementation:** Add a new module under `src/datadog_mcp/tools/` (or extend an existing one). Use the shared client from `client.get_api_client()` and return JSON strings; on `ApiException` return `{"error": errors.sanitize_error(e)}`.
3. **Registration:** Register the tool in [src/datadog_mcp/server.py](src/datadog_mcp/server.py) with `@mcp.tool()` and a clear docstring (parameters, scope, returns).
4. **Documentation:** Add the tool to the README table and to [docs/tool_reference.md](docs/tool_reference.md) (parameters, scopes, returns).

## Adding a resource

1. Add a function in [src/datadog_mcp/resources.py](src/datadog_mcp/resources.py) that returns JSON (reuse tool logic where possible).
2. Register with `@mcp.resource("datadog://...")` in server.py.
3. Update [docs/api_mapping.md](docs/api_mapping.md) and README Resources section.

## Adding a prompt

1. Add a function that fetches data (via existing get_* tools or resources), then builds a prompt string for the LLM.
2. Register with `@mcp.prompt()` in server.py.
3. Document in api_mapping.md (Prompts table) and README.

## Testing

- Run the full suite: `uv run pytest`
- Tests live in `tests/`; use `respx` to mock the DataDog API when testing tools without real credentials.
- Do not log or commit API keys; use fixtures (e.g. `mock_dd_env`) to set fake env vars in tests.

## Secrets

Do **not** log, echo, or commit `DD_API_KEY` or `DD_APP_KEY`. Use environment variables or a secure secret manager only. See [errors.py](src/datadog_mcp/errors.py) for sanitization of error messages.

## Architecture

See [docs/architecture.md](docs/architecture.md) for component overview and data flow. If this repo is used from a workspace that has a REFERENCE_INDEX, add pointers there as needed.

## Pull requests

Open a PR with a clear description. Ensure tests pass and docs (api_mapping.md, tool_reference.md, README) are updated for any new tools, resources, or prompts.
