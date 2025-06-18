#!/usr/bin/env python3
import os
import requests
from datetime import datetime, timedelta, timezone

# Config from environment (or default)
ES_URL     = os.getenv("ES_URL", "http://localhost:9200")
INDEX      = os.getenv("ES_INDEX", "audit-logs-*")
LOOKBACK   = int(os.getenv("LOOKBACK_MIN", "5"))
REPO       = os.getenv("GITHUB_REPO", "snarls94/analytics-prep")
SITE_URL   = os.getenv("SITE_URL", "https://snarls94.github.io/analytics-prep/")
GITHUB_PAT = os.getenv("GITHUB_TOKEN")  # your classic PAT with public_repo

def main():
    now   = datetime.now(timezone.utc)
    since = now - timedelta(minutes=LOOKBACK)

    # Build the ES DSL query
    es_query = {
      "query": {
        "bool": {
          "must": [
            { "term": { "event.keyword": "UNAUTHORIZED_ACCESS" } },
            { "range": { "timestamp": {
                "gte": since.isoformat(), 
                "lte": now.isoformat() } } }
          ]
        }
      }
    }

    # Direct REST call
    url  = f"{ES_URL}/{INDEX}/_search"
    resp = requests.post(url, json=es_query)
    resp.raise_for_status()
    hits = resp.json()["hits"]["total"]["value"]

    print("DEBUG: Starting check_unauth_alert.py")
    print(f"DEBUG: Found {hits} UNAUTHORIZED_ACCESS events in the last {LOOKBACK} minutes")

    if hits > 0:
        issue_url = f"https://api.github.com/repos/{REPO}/issues"
        headers   = {
          "Authorization": f"token {GITHUB_PAT}",
          "Accept": "application/vnd.github+json"
        }
        body = {
          "title": "Post-Incident Policy Review",
          "body": (
            f"Detected **{hits}** unauthorized‐access event(s) between "
            f"{since.isoformat()} and {now.isoformat()}.\n\n"
            f"Please review: {SITE_URL}"
          )
        }
        r = requests.post(issue_url, json=body, headers=headers)
        r.raise_for_status()
        print(f"⚠️ Created GitHub issue: {body['title']}")

if __name__ == "__main__":
    main()
