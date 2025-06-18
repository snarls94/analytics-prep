-- 0002_partition_audit_events.sql
-- Convert audit_events to RANGE partitioning by event_timestamp

BEGIN;

-- 1) Rename the existing table out of the way
ALTER TABLE audit_events RENAME TO audit_events_raw;

-- 2) Create the new partitioned parent
CREATE TABLE audit_events (
    event_id        SERIAL        PRIMARY KEY,
    event_type      VARCHAR(50)   NOT NULL,
    event_timestamp TIMESTAMPTZ   NOT NULL,
    user_id         VARCHAR(100)  NOT NULL,
    outcome         VARCHAR(20)   NOT NULL
        CHECK (outcome IN ('SUCCESS','FAILURE')),
    source_system   VARCHAR(100),
    system_name     VARCHAR(100),
    system_location VARCHAR(100)  NOT NULL,
    metadata        JSONB
) PARTITION BY RANGE (event_timestamp);

-- 3) Attach an initial “catch-all” partition for existing data
CREATE TABLE audit_events_initial PARTITION OF audit_events
  FOR VALUES FROM ('0001-01-01') TO ('9999-12-31');
INSERT INTO audit_events_initial SELECT * FROM audit_events_raw;
DROP TABLE audit_events_raw;

-- 4) Create a template for future monthly partitions
-- (you can repeat these CREATEs for each month you need)
CREATE TABLE IF NOT EXISTS audit_events_2025_06 PARTITION OF audit_events
  FOR VALUES FROM ('2025-06-01') TO ('2025-07-01');

CREATE TABLE IF NOT EXISTS audit_events_2025_07 PARTITION OF audit_events
  FOR VALUES FROM ('2025-07-01') TO ('2025-08-01');

-- …and so on for each month…

COMMIT;
