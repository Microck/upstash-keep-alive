"""Upstash Redis keep-alive utility.

Prevents Upstash from archiving idle Redis databases by periodically
performing actual data operations (SET + EXPIRE). Upstash requires real
data commands — PING alone does not count as activity for archival prevention.

Typical usage with a cron scheduler (e.g., every 30 days):
    python keep_alive.py

Required environment variables:
    UPSTASH_REDIS_REST_URL   — Upstash Redis REST API URL
    UPSTASH_REDIS_REST_TOKEN — Upstash Redis REST API token

Optional environment variables (with defaults):
    KEEPALIVE_KEY            — Redis key used for the keep-alive value (default: "upstash-keepalive")
    KEEPALIVE_EXPIRY_SECONDS — TTL for the keep-alive key in seconds (default: 2592000, i.e., 30 days)
    REQUEST_TIMEOUT_SECONDS  — HTTP request timeout in seconds (default: 10)
"""

import datetime
import os
import sys
import time

import requests

# Configuration from environment variables
UPSTASH_REDIS_REST_URL = os.getenv("UPSTASH_REDIS_REST_URL")
"""Upstash Redis REST API URL (e.g., 'https://us1-xxx-xxxxx.upstash.io')."""

UPSTASH_REDIS_REST_TOKEN = os.getenv("UPSTASH_REDIS_REST_TOKEN")
"""Upstash Redis REST API authentication token."""

KEEPALIVE_KEY = os.getenv("KEEPALIVE_KEY", "upstash-keepalive")
"""Redis key name used to store the keep-alive ping value."""

KEEPALIVE_EXPIRY_SECONDS = int(os.getenv("KEEPALIVE_EXPIRY_SECONDS", "2592000"))
"""TTL in seconds for the keep-alive key. Defaults to 30 days (2,592,000 seconds)."""

REQUEST_TIMEOUT_SECONDS = int(os.getenv("REQUEST_TIMEOUT_SECONDS", "10"))
"""HTTP request timeout in seconds for Upstash REST API calls."""


def keep_alive() -> bool:
    """Keep Upstash Redis database active by performing actual data operations.

    Note: PING command does NOT count as activity for archival purposes.
    We must perform actual data operations (SET, GET, EXPIRE, etc.) to prevent archiving.

    Returns:
        True if the keep-alive succeeded, False otherwise.
    """
    if not UPSTASH_REDIS_REST_URL or not UPSTASH_REDIS_REST_TOKEN:
        print(
            "Error: UPSTASH_REDIS_REST_URL and UPSTASH_REDIS_REST_TOKEN environment variables are required."
        )
        return False

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    headers = {
        "Authorization": f"Bearer {UPSTASH_REDIS_REST_TOKEN}",
    }

    try:
        key = KEEPALIVE_KEY
        value = f"ping-{int(time.time())}"

        url = f"{UPSTASH_REDIS_REST_URL.rstrip('/')}/set/{key}/{value}/ex/{KEEPALIVE_EXPIRY_SECONDS}"

        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT_SECONDS)

        if response.status_code == 200:
            print(
                f"[{timestamp}] Success! Database activity recorded. Key '{key}' set with 30-day expiry."
            )
            return True
        else:
            print(f"[{timestamp}] Warning: Status {response.status_code}")
            print(response.text)
            return False
    except requests.ConnectionError as error:
        print(f"[{timestamp}] Connection failed: {error}")
        return False
    except requests.Timeout as error:
        print(f"[{timestamp}] Request timed out: {error}")
        return False
    except requests.RequestException as error:
        print(f"[{timestamp}] Request failed: {error}")
        return False


if __name__ == "__main__":
    # Exit code 0 on success, 1 on failure — suitable for cron health checks
    success = keep_alive()
    sys.exit(0 if success else 1)
