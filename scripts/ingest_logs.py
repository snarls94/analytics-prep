#!/usr/bin/env python3
"""
scripts/ingest_logs.py
ETL: validate and load audit_log CSVs into audit_events.
"""

import os
import glob
import pandas as pd
from sqlalchemy import create_engine

# Config
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/yourdb")
RAW_GLOB     = "data/raw/audit_log_*.csv"
TABLE_NAME   = "audit_events"

# Required columns per AU-3
REQUIRED_COLS = [
    "event_type",
    "event_timestamp",
    "user_id",
    "outcome",
    "source_system",
    "system_name",
    "system_location",
]

def main():
    engine = create_engine(DATABASE_URL)
    files = glob.glob(RAW_GLOB) + ["data/raw/sample_audit.csv"]
    if not files:
        print("No raw CSVs found. Place files matching audit_log_*.csv or sample_audit.csv in data/raw/")
        return

    for path in files:
        print(f"Loading {path}…")
        df = pd.read_csv(path)

        # Validate required columns
        missing = [c for c in REQUIRED_COLS if c not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns in {path}: {missing}")

        # Rename timestamp field if needed
        if "timestamp" in df.columns:
            df = df.rename(columns={"timestamp": "event_timestamp"})

        # Append to DB by passing the DATABASE_URL string directly
        df.to_sql(
            name=TABLE_NAME,
            con=DATABASE_URL,     # let pandas/SQLAlchemy create its own engine
            if_exists="append",
            index=False,
            method="multi",       # still use batched INSERT
            chunksize=1000
        )
        print(f"  → {len(df)} rows inserted into {TABLE_NAME}.")

if __name__ == "__main__":
    main()
