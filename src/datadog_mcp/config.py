"""Load and validate configuration from environment. No secrets in code."""

import os


def get_config() -> dict:
    """
    Read DataDog config from environment.
    Raises ValueError with a clear message if required keys are missing.
    """
    api_key = os.environ.get("DD_API_KEY", "").strip()
    app_key = os.environ.get("DD_APP_KEY", "").strip()
    site = os.environ.get("DD_SITE", "datadoghq.com").strip() or "datadoghq.com"

    if not api_key:
        raise ValueError(
            "DD_API_KEY is required. Set it in the environment or in a .env file. "
            "Create keys at https://app.datadoghq.com/organization-settings/api-keys"
        )
    if not app_key:
        raise ValueError(
            "DD_APP_KEY is required. Set it in the environment or in a .env file. "
            "Create keys at https://app.datadoghq.com/organization-settings/api-keys"
        )

    return {
        "api_key": api_key,
        "app_key": app_key,
        "site": site,
    }
