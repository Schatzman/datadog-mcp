"""
Retry with backoff on 429 (rate limit). Wraps ApiClient.call_api so all API calls benefit.
"""

import time
from typing import Any, Dict, List, Optional, Tuple

from datadog_api_client import ApiClient
from datadog_api_client.configuration import Configuration
from datadog_api_client.exceptions import ApiException

# Max retries after the first attempt (so 2 retries = up to 3 total requests)
DEFAULT_MAX_RETRIES = 2
# Backoff: 1s, then 2s (exponential 1 * 2^attempt)
DEFAULT_INITIAL_BACKOFF_SEC = 1.0


class RetryingApiClient(ApiClient):
    """
    ApiClient that retries on HTTP 429 (rate limit) with exponential backoff.
    """

    def __init__(
        self,
        configuration: Configuration,
        max_retries: int = DEFAULT_MAX_RETRIES,
        initial_backoff_sec: float = DEFAULT_INITIAL_BACKOFF_SEC,
    ):
        super().__init__(configuration)
        self._max_retries = max_retries
        self._initial_backoff_sec = initial_backoff_sec

    def call_api(
        self,
        resource_path: str,
        method: str,
        path_params: Optional[Dict[str, Any]] = None,
        query_params: Optional[List[Tuple[str, Any]]] = None,
        header_params: Optional[Dict[str, Any]] = None,
        body: Optional[Any] = None,
        post_params: Optional[List[Tuple[str, Any]]] = None,
        files: Optional[Dict[str, List]] = None,
        response_type: Optional[Tuple[Any]] = None,
        return_http_data_only: Optional[bool] = None,
        collection_formats: Optional[Dict[str, str]] = None,
        preload_content: bool = True,
        request_timeout: Optional[Any] = None,
        host: Optional[str] = None,
        check_type: Optional[bool] = None,
    ):
        last_exception = None
        for attempt in range(self._max_retries + 1):
            try:
                return super().call_api(
                    resource_path=resource_path,
                    method=method,
                    path_params=path_params,
                    query_params=query_params,
                    header_params=header_params,
                    body=body,
                    post_params=post_params,
                    files=files,
                    response_type=response_type,
                    return_http_data_only=return_http_data_only,
                    collection_formats=collection_formats,
                    preload_content=preload_content,
                    request_timeout=request_timeout,
                    host=host,
                    check_type=check_type,
                )
            except ApiException as e:
                last_exception = e
                if getattr(e, "status", None) == 429 and attempt < self._max_retries:
                    backoff = self._initial_backoff_sec * (2**attempt)
                    time.sleep(backoff)
                    continue
                raise
        if last_exception is not None:
            raise last_exception
        raise RuntimeError("Retry loop exited without returning or raising")
