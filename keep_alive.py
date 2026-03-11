import datetime
import os
import time

import requests

UPSTASH_REDIS_REST_URL = os.getenv("UPSTASH_REDIS_REST_URL")
UPSTASH_REDIS_REST_TOKEN = os.getenv("UPSTASH_REDIS_REST_TOKEN")


def keep_alive() -> None:
    """Keep Upstash Redis database active by performing actual data operations.

    Note: PING command does NOT count as activity for archival purposes.
    We must perform actual data operations (SET, GET, EXPIRE, etc.) to prevent archiving.
    """
    if not UPSTASH_REDIS_REST_URL or not UPSTASH_REDIS_REST_TOKEN:
        print(
            "Error: UPSTASH_REDIS_REST_URL and UPSTASH_REDIS_REST_TOKEN environment variables are required."
        )
        return

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    headers = {
        "Authorization": f"Bearer {UPSTASH_REDIS_REST_TOKEN}",
    }

    try:
        # Use SET with EXPIRE - this counts as actual activity
        # We set a key that expires after 30 days (2592000 seconds)
        key = "upstash-keepalive"
        value = f"ping-{int(time.time())}"

        # SET with EXPIRE in one command using the Upstash REST API format
        url = f"{UPSTASH_REDIS_REST_URL.rstrip('/')}/set/{key}/{value}/ex/2592000"

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            print(
                f"[{timestamp}] Success! Database activity recorded. Key '{key}' set with 30-day expiry."
            )
        else:
            print(f"[{timestamp}] Warning: Status {response.status_code}")
            print(response.text)
    except Exception as error:
        print(f"[{timestamp}] Failed: {str(error)}")


if __name__ == "__main__":
    keep_alive()
