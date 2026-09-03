from datetime import datetime

from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.operators.bash import BashOperator

SCRIPTS_PATH = "/opt/airflow/scripts"


def run_repair_reviews():
    import sys
    sys.path.insert(0, SCRIPTS_PATH)
    from repair_reviews import repair_reviews

    repair_reviews(
        input_path="/opt/airflow/data/olist_order_reviews_dataset.csv",
        output_path="/opt/airflow/data/cleaned_data/olist_order_reviews_dataset.csv",
    )


def run_ingestion():
    import sys
    sys.path.insert(0, SCRIPTS_PATH)
    from load_to_bigquery import main

    main()


with DAG(
    dag_id="olist_pipeline",
    start_date=datetime(2026, 8, 27),
    schedule="*/5 * * * *",
    catchup=False,
    tags=["olist", "bigquery", "dbt"],
) as dag:

    repair_reviews_task = PythonOperator(
        task_id="repair_reviews",
        python_callable=run_repair_reviews,
    )

    ingest_to_bigquery = PythonOperator(
        task_id="ingest_to_bigquery",
        python_callable=run_ingestion,
    )

    dbt_transform = BashOperator(
        task_id="dbt_transform",
        bash_command="""
        cd /opt/airflow/olist_dbt &&
        dbt run \
          --profiles-dir /opt/airflow/olist_dbt \
          --project-dir /opt/airflow/olist_dbt
        """,
    )

    repair_reviews_task >> ingest_to_bigquery >> dbt_transform