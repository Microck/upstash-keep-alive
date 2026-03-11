# upstash redis keep-alive

python script to keep your upstash redis database from being archived for inactivity.

upstash docs mention free tier databases are archived after a minimum of 14 days of inactivity.

## important: why the old version didn't work

**the previous version used the `PING` command, which does NOT count as database activity.**

upstash only considers actual data operations (SET, GET, EXPIRE, etc.) as activity. simply pinging the database endpoint is not enough to prevent archival.

this updated version uses `SET` with an `EXPIRE` to actually write data, which counts as real activity.

## how it works

performs a `SET` operation with a 30-day expiration on a `upstash-keepalive` key. this creates actual database activity that upstash recognizes, preventing the 14-day archival.

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

## automate with github actions (recommended)

the included github actions workflow runs every 2 days automatically.

### setup steps:

1. fork or clone this repo
2. go to your repo's **settings > secrets and variables > actions**
3. add two repository secrets:
   - `UPSTASH_REDIS_REST_URL` - your upstash redis rest url
   - `UPSTASH_REDIS_REST_TOKEN` - your upstash redis rest token

4. the workflow will run automatically every 2 days

you can also trigger it manually from the **actions** tab by clicking "run workflow".

## automate with cron

if you prefer to run this on your own server, add to crontab (`crontab -e`) to run every 2 days:

```bash
0 0 */2 * * /usr/bin/python3 /path/to/keep_alive.py >> /var/log/upstash_keep_alive.log 2>&1
```

## frequency recommendations

- **run at least every 7-10 days** to stay safely under the 14-day threshold
- the github actions workflow runs every 2 days for extra safety

## references

- https://upstash.com/docs/redis/features/restapi
- https://upstash.com/docs/redis/help/faq (see "what happens if my database is not used?")
