-- 0001_create_audit_events.sql
-- CJIS Audit Events table (AU-2 & AU-3)

CREATE TABLE IF NOT EXISTS audit_events (
    event_id        SERIAL PRIMARY KEY,
    event_type      VARCHAR(50)    NOT NULL,  -- e.g. "LOGIN", "VIEW_RECORD", “DELETE_PERMISSION”, etc.
    event_timestamp TIMESTAMPTZ     NOT NULL,  -- when the event occurred (must be timezone‐aware)
    user_id         VARCHAR(100)   NOT NULL,  -- who performed it
    outcome         VARCHAR(20)     NOT NULL
        CONSTRAINT chk_audit_events_outcome 
        CHECK (outcome IN ('SUCCESS','FAILURE')),  -- enforce only SUCCESS or FAILURE
    source_system   VARCHAR(100),  -- service or application name
    system_name     VARCHAR(100),  -- Application component or host
    system_location VARCHAR(100)   NOT NULL,  -- “where” (data center, hostname, etc.)
    metadata        JSONB          -- any extra context
);

-- Indexes for efficient querying & retention
CREATE INDEX IF NOT EXISTS idx_audit_events_timestamp
    ON audit_events (event_timestamp);

CREATE INDEX IF NOT EXISTS idx_audit_events_user
    ON audit_events (user_id);

CREATE INDEX IF NOT EXISTS idx_audit_events_event_type
    ON audit_events (event_type);

CREATE INDEX IF NOT EXISTS idx_audit_events_outcome
    ON audit_events (outcome);

CREATE INDEX IF NOT EXISTS idx_audit_events_location
    ON audit_events (system_location);

-- TODO: consider partitioning audit_events by event_timestamp for 1-year data retention
