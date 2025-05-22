#!/usr/bin/env python3
import os
import requests
from elasticsearch import Elasticsearch
from datetime import datetime, timedelta, timezone

# Config from environment (or default)
ES_URL     = os.getenv("ES_URL", "http://localhost:9200")
INDEX      = os.getenv("ES_INDEX", "audit-logs-*")
LOOKBACK   = int(os.getenv("LOOKBACK_MIN", "5"))
REPO       = os.getenv("GITHUB_REPO", "snarls94/analytics-prep")
SITE_URL   = os.getenv("SITE_URL", "https://snarls94.github.io/analytics-prep/")
GITHUB_PAT = os.getenv("GITHUB_TOKEN")  # set this in your env

def main():
    es = Elasticsearch(ES_URL)
    # timezone‐aware "now" in UTC
    now = datetime.now(timezone.utc)
    since = now - timedelta(minutes=LOOKBACK)

    # Build the ES query
    query = {
        "bool": {
            "must": [
                {"term": {"event.keyword": "UNAUTHORIZED_ACCESS"}},
                {"range": {
                    "timestamp": {
                        "gte": since.isoformat(),
                        "lte": now.isoformat()
                    }
                }}
            ]
        }
    }

    resp = es.search(index=INDEX, query=query)
    count = resp["hits"]["total"]["value"]
    print(f"DEBUG: Found {count} UNAUTHORIZED_ACCESS events in the last {LOOKBACK} minutes")

    if count > 0:
        url = f"https://api.github.com/repos/{REPO}/issues"
        headers = {
            "Authorization": f"token {GITHUB_PAT}",
            "Accept": "application/vnd.github+json"
        }
        body = {
            "title": "Post-Incident Policy Review",
            "body": (
                f"Detected **{count}** unauthorized‐access event(s) between "
                f"{since.isoformat()} and {now.isoformat()}.\n\n"
                f"Please review: {SITE_URL}"
            )
        }
        r = requests.post(url, json=body, headers=headers)
        r.raise_for_status()
        print(f"⚠️ Created GitHub issue: {body['title']}")

if __name__ == "__main__":
    main()
