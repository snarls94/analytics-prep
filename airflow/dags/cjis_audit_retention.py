# airflow/cjis_audit_retention.py

from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator

default_args = {
    'owner': 'analytics',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='cjis_audit_retention',
    default_args=default_args,
    schedule_interval='@daily',  # run once a day
    catchup=False,
    tags=['cjis', 'audit', 'retention'],
) as dag:

    purge_old_events = PostgresOperator(
        task_id='purge_old_audit_events',
        postgres_conn_id='postgres_default',  # configure this in Airflow UI → Admin → Connections
        sql="""
            DELETE FROM audit_events
            WHERE event_timestamp < NOW() - INTERVAL '1 year';
        """,
    )

    purge_old_events
