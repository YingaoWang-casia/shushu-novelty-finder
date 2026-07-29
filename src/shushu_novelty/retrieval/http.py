"""Small HTTP client with bounded retries and explicit failures."""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from email.message import Message
from typing import Any

from shushu_novelty.errors import RetrievalError

RETRYABLE_STATUS = {429, 500, 502, 503, 504}


def _retry_delay(headers: Message | None, attempt: int, backoff: float) -> float:
    if headers is not None:
        value = headers.get("Retry-After")
        if value:
            try:
                return min(float(value), 30.0)
            except ValueError:
                pass
    return min(backoff * (2**attempt), 30.0)


def get_json(
    url: str,
    headers: dict[str, str] | None = None,
    timeout: float = 30.0,
    retries: int = 2,
    backoff: float = 1.0,
) -> dict[str, Any]:
    request = urllib.request.Request(url, headers=headers or {})
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                value = json.loads(response.read())
            if not isinstance(value, dict):
                raise RetrievalError(f"expected JSON object from {url}")
            return value
        except urllib.error.HTTPError as exc:
            if exc.code not in RETRYABLE_STATUS or attempt == retries:
                raise RetrievalError(f"HTTP {exc.code} from {url}") from exc
            time.sleep(_retry_delay(exc.headers, attempt, backoff))
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            if attempt == retries:
                raise RetrievalError(f"request failed for {url}: {exc}") from exc
            time.sleep(_retry_delay(None, attempt, backoff))
    raise AssertionError("retry loop exhausted without returning or raising")
