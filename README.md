# upstash-redis-keep-alive

Python script to keep your Upstash Redis database from being archived for inactivity.

Upstash archives free-tier databases after 14 days of inactivity. **PING does not count** — only actual data operations (SET, GET, etc.) prevent archival.

This script performs a `SET` with a 30-day expiry on a `upstash-keepalive` key, creating real database activity.

## Quick start

```bash
pip install -r requirements.txt
export UPSTASH_REDIS_REST_URL="https://your-database.upstash.io"
export UPSTASH_REDIS_REST_TOKEN="your-rest-token"
python keep_alive.py
```

## Automation

### GitHub Actions

Create `.github/workflows/keep-alive.yml`:

```yaml
name: Upstash Keep-Alive
on:
  schedule:
    - cron: "0 0 */2 * *"  # every 2 days
  workflow_dispatch:
jobs:
  keep-alive:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt
      - run: python keep_alive.py
        env:
          UPSTASH_REDIS_REST_URL: ${{ secrets.UPSTASH_REDIS_REST_URL }}
          UPSTASH_REDIS_REST_TOKEN: ${{ secrets.UPSTASH_REDIS_REST_TOKEN }}
```

Add `UPSTASH_REDIS_REST_URL` and `UPSTASH_REDIS_REST_TOKEN` as repository secrets under **Settings > Secrets and variables > Actions**.

### Cron

```bash
0 0 */2 * * /usr/bin/python3 /path/to/keep_alive.py >> /var/log/upstash_keep_alive.log 2>&1
```

## Why not PING?

Upstash only considers data operations as activity. PING returns `PONG` but does not reset the inactivity timer. See [Upstash FAQ](https://upstash.com/docs/redis/help/faq) ("What happens if my database is not used?").

## References

- [Upstash REST API docs](https://upstash.com/docs/redis/features/restapi)
- [Upstash FAQ](https://upstash.com/docs/redis/help/faq)
