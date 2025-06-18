#!/usr/bin/env python3
"""
scripts/validate_audit.py
Validate sample_audit.csv rows against the required audit record shape.
"""

import sys
import pandas as pd
from pydantic import BaseModel, ValidationError
from datetime import datetime

class AuditRecord(BaseModel):
    event_type: str
    event_timestamp: datetime
    user_id: str
    outcome: str
    source_system: str
    system_name: str
    system_location: str

    class Config:
        extra = "ignore"

def main():
    df = pd.read_csv("data/raw/sample_audit.csv")
    errors = []
    for idx, row in df.iterrows():
        try:
            AuditRecord(**row.to_dict())
        except ValidationError as e:
            errors.append(f"Row {idx}: {e}")

    if errors:
        print("Validation failed:")
        for err in errors:
            print(err)
        sys.exit(1)
    else:
        print(f"All {len(df)} rows passed validation.")

if __name__ == "__main__":
    main()
