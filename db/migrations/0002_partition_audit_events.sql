BEGIN;

-- 1) Rename the old table out of the way
ALTER TABLE audit_events RENAME TO audit_events_raw;

-- 2) Create the new partitioned parent with composite PK
CREATE TABLE audit_events (
    event_id        SERIAL        NOT NULL,
    event_type      VARCHAR(50)   NOT NULL,
    event_timestamp TIMESTAMPTZ   NOT NULL,
    user_id         VARCHAR(100)  NOT NULL,
    outcome         VARCHAR(20)   NOT NULL
        CHECK (outcome IN ('SUCCESS','FAILURE')),
    source_system   VARCHAR(100),
    system_name     VARCHAR(100),
    system_location VARCHAR(100)  NOT NULL,
    metadata        JSONB,
    PRIMARY KEY (event_id, event_timestamp)
) PARTITION BY RANGE (event_timestamp);

-- 3) Create the partitions **you know** you need for existing data
CREATE TABLE IF NOT EXISTS audit_events_2025_06 PARTITION OF audit_events
  FOR VALUES FROM ('2025-06-01') TO ('2025-07-01');
CREATE TABLE IF NOT EXISTS audit_events_2025_07 PARTITION OF audit_events
  FOR VALUES FROM ('2025-07-01') TO ('2025-08-01');

-- 4) Catch-all default for anything else
CREATE TABLE audit_events_default PARTITION OF audit_events DEFAULT;

-- 5) Move the old rows into the new structure
INSERT INTO audit_events SELECT * FROM audit_events_raw;
DROP TABLE audit_events_raw;

COMMIT;
