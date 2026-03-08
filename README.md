# upstash redis keep-alive

python script to keep your upstash redis database from being archived for inactivity.

upstash docs mention free tier databases are archived after a minimum of 14 days of inactivity.

## how it works

calls `PING` over upstash redis REST API (`/ping`). this counts as database activity.

## setup

### 1. install dependencies

```bash
pip install -r requirements.txt
```

### 2. set environment variables

```bash
export UPSTASH_REDIS_REST_URL="https://your-database.upstash.io"
export UPSTASH_REDIS_REST_TOKEN="your-rest-token"
```

### 3. run script

```bash
python keep_alive.py
```

## automate with cron

add to crontab (`crontab -e`) to run daily:

```bash
0 8 * * * /usr/bin/python3 /path/to/keep_alive.py >> /var/log/upstash_keep_alive.log 2>&1
```

### github actions

you can run this from github actions instead of a vps.

## references

- https://upstash.com/docs/redis/features/restapi
- https://upstash.com/docs/redis/help/faq
