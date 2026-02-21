"""
Centralized error handling for DataDog API calls.
Never log or return API keys or raw stack traces.
"""

from datadog_api_client.exceptions import ApiException


def sanitize_error(exc: Exception) -> str:
    """Return a safe user-facing message. Strips any key/credential hints."""
    msg = str(exc).strip()
    # Avoid leaking status codes that might contain sensitive info in URLs
    if "api_key" in msg.lower() or "403" in msg or "401" in msg:
        return "DataDog API authentication failed or insufficient permissions."
    if "429" in msg:
        return "DataDog API rate limit exceeded. Retry later."
    if len(msg) > 500:
        return msg[:500] + "..."
    return msg or "DataDog API request failed."


def wrap_dd_api(f):
    """Decorator that catches ApiException and re-raises with sanitized message."""

    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ApiException as e:
            raise ValueError(sanitize_error(e)) from None
        except ValueError:
            raise
        except Exception as e:
            raise ValueError(sanitize_error(e)) from None

    return inner
