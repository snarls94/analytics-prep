-- 0002_create_monthly_partitions.sql
-- Create May 2025 partition for audit_events
CREATE TABLE IF NOT EXISTS audit_events_y2025m05 
  PARTITION OF audit_events
    FOR VALUES FROM ('2025-05-01') TO ('2025-06-01');