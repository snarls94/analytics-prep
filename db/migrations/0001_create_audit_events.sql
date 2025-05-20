-- 0001_create_audit_events.sql
-- CJIS Audit Events table

CREATE TABLE IF NOT EXISTS audit_events (
    event_id        SERIAL PRIMARY KEY,
    event_type      VARCHAR(50)  NOT NULL,         -- e.g. "LOGIN", "VIEW_RECORD"
    event_timestamp TIMESTAMPTZ   NOT NULL,         -- when the event occurred
    user_id         VARCHAR(100)  NOT NULL,         -- who performed it
    outcome         VARCHAR(20)   NOT NULL,         -- e.g. "SUCCESS", "FAILURE"
    source_system   VARCHAR(100),                   -- microservice or module
    system_name     VARCHAR(100),                   -- eAgent component
    metadata        JSONB                             -- any extra context
);

-- Retention: keep at least 12 months
CREATE INDEX IF NOT EXISTS idx_audit_events_timestamp
    ON audit_events (event_timestamp);
