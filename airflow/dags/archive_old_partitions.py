# airflow/dags/archive_old_partitions.py

from airflow import DAG
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta, timezone

default_args = {
    'owner': 'sruthi',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='cjis_archive_old_partitions',
    default_args=default_args,
    schedule_interval='@monthly',
    catchup=False,
    tags=['cjis','archive'],
) as dag:

    @task
    def find_old_partitions():
        pg = PostgresHook(postgres_conn_id='postgres_default')
        # threshold: first of the month, 12 months ago
        cutoff = (datetime.now(timezone.utc).replace(day=1) - timedelta(days=365)).replace(day=1)
        # fetch all child partitions of audit_events
        sql = """
        SELECT c.relname
          FROM pg_inherits i
          JOIN pg_class c ON i.inhrelid = c.oid
         WHERE i.inhparent = 'audit_events'::regclass;
        """
        rows = pg.get_records(sql)
        old_parts = []
        for (part,) in rows:
            # expect names like 'audit_events_2024_06'
            suffix = part.replace('audit_events_', '')
            try:
                part_date = datetime.strptime(suffix, '%Y_%m')
                if part_date < cutoff:
                    old_parts.append(part)
            except ValueError:
                # skip anything unexpected
                continue
        return old_parts

    @task
    def archive_and_drop(partitions: list[str]):
        pg = PostgresHook(postgres_conn_id='postgres_default')
        for part in partitions:
            # In a real DAG you'd: COPY TO CSV → upload to MinIO
            print(f"🔒 Would archive partition: {part}")
            # then detach & drop:
            pg.run(f"ALTER TABLE audit_events DETACH PARTITION {part}")
            pg.run(f"DROP TABLE IF EXISTS {part}")
            print(f"🗑️  Dropped partition: {part}")

    parts = find_old_partitions()
    archive_and_drop(parts)
