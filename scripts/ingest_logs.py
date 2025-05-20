#!/usr/bin/env python3
"""
scripts/ingest_logs.py
ETL: load audit_log CSVs into the audit_events table in PostgreSQL.
"""

import os
import glob
import pandas as pd
from sqlalchemy import create_engine

# Config
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/yourdb")
RAW_GLOB     = "data/raw/audit_log_*.csv"
TABLE_NAME   = "audit_events"

def main():
    engine = create_engine(DATABASE_URL)
    files = glob.glob(RAW_GLOB)
    if not files:
        print("No raw CSVs found. Make sure data/raw/ contains audit_log_*.csv")
        return

    for path in files:
        print(f"Loading {path}…")
        df = pd.read_csv(path)

        # Rename timestamp column to match DDL
        if "timestamp" in df.columns:
            df = df.rename(columns={"timestamp": "event_timestamp"})

        # Append to DB
        df.to_sql(
            TABLE_NAME,
            engine,
            if_exists="append",
            index=False,
            method="multi",
            chunksize=1000
        )
        print(f"  → {len(df)} rows inserted.")

if __name__ == "__main__":
    main()
