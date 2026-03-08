import datetime
import os

import requests

UPSTASH_REDIS_REST_URL = os.getenv("UPSTASH_REDIS_REST_URL")
UPSTASH_REDIS_REST_TOKEN = os.getenv("UPSTASH_REDIS_REST_TOKEN")


def ping_upstash_redis() -> None:
    if not UPSTASH_REDIS_REST_URL or not UPSTASH_REDIS_REST_TOKEN:
        print(
            "Error: UPSTASH_REDIS_REST_URL and UPSTASH_REDIS_REST_TOKEN environment variables are required."
        )
        return

    url = f"{UPSTASH_REDIS_REST_URL.rstrip('/')}/ping"
    headers = {
        "Authorization": f"Bearer {UPSTASH_REDIS_REST_TOKEN}",
        "Content-Type": "application/json",
    }

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            print(f"[{timestamp}] Success! Active. Response: {response.text}")
        else:
            print(f"[{timestamp}] Warning: Status {response.status_code}")
            print(response.text)
    except Exception as error:
        print(f"[{timestamp}] Failed: {str(error)}")


if __name__ == "__main__":
    ping_upstash_redis()
