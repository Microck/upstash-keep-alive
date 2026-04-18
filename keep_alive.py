import datetime
import os
import sys
import time

import requests

UPSTASH_REDIS_REST_URL = os.getenv("UPSTASH_REDIS_REST_URL")
UPSTASH_REDIS_REST_TOKEN = os.getenv("UPSTASH_REDIS_REST_TOKEN")
KEEPALIVE_KEY = os.getenv("KEEPALIVE_KEY", "upstash-keepalive")
KEEPALIVE_EXPIRY_SECONDS = int(os.getenv("KEEPALIVE_EXPIRY_SECONDS", "2592000"))
REQUEST_TIMEOUT_SECONDS = int(os.getenv("REQUEST_TIMEOUT_SECONDS", "10"))

HTTP_OK = 200


def keep_alive() -> bool:
    """Keep Upstash Redis database active by performing actual data operations.

    Note: PING command does NOT count as activity for archival purposes.
    We must perform actual data operations (SET, GET, EXPIRE, etc.)
    to prevent archiving.

    Returns:
        True if the keep-alive succeeded, False otherwise.
    """
    if not UPSTASH_REDIS_REST_URL or not UPSTASH_REDIS_REST_TOKEN:
        print(
            "Error: UPSTASH_REDIS_REST_URL and"
            " UPSTASH_REDIS_REST_TOKEN environment variables are required.",
        )
        return False

    timestamp = datetime.datetime.now(tz=datetime.timezone.utc).strftime(
        "%Y-%m-%d %H:%M:%S",
    )
    headers = {
        "Authorization": f"Bearer {UPSTASH_REDIS_REST_TOKEN}",
    }

    try:
        key = KEEPALIVE_KEY
        value = f"ping-{int(time.time())}"

        url = (
            f"{UPSTASH_REDIS_REST_URL.rstrip('/')}"
            f"/set/{key}/{value}/ex/{KEEPALIVE_EXPIRY_SECONDS}"
        )

        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT_SECONDS)

        if response.status_code == HTTP_OK:
            print(
                f"[{timestamp}] Success! Database activity recorded."
                f" Key '{key}' set with 30-day expiry.",
            )
            return True
        else:  # noqa: RET505
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
    success = keep_alive()
    sys.exit(0 if success else 1)
