import os
from pathlib import Path

from google.cloud import bigquery


# Airflow container paths
CREDENTIALS_FILE = "/opt/airflow/credentials/service-account.json"
DATA_FOLDER = Path("/opt/airflow/data")
CLEANED_DATA_FOLDER = Path("/opt/airflow/data/cleaned_data")
DATASET_ID = "raw_sales"

REVIEWS_FILENAME = "olist_order_reviews_dataset.csv"


def load_csvs_to_bigquery():
    """Load all CSV files from the data directory into BigQuery."""

    # Make credentials explicit for the Airflow container
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_FILE

    client = bigquery.Client()
    project_id = client.project

    failed_files = []

    csv_files = sorted(DATA_FOLDER.glob("*.csv"))

    if not csv_files:
        raise FileNotFoundError(
            f"No CSV files found in {DATA_FOLDER}"
        )

    print(f"Found {len(csv_files)} CSV files.")
    print(f"Target dataset: {project_id}.{DATASET_ID}")

    for csv_file in csv_files:
        table_name = csv_file.stem.replace("_dataset", "")
        table_id = f"{project_id}.{DATASET_ID}.{table_name}"

        # Use the repaired reviews file instead of the raw one, if available
        source_file_path = csv_file
        if csv_file.name == REVIEWS_FILENAME:
            cleaned_candidate = CLEANED_DATA_FOLDER / REVIEWS_FILENAME
            if cleaned_candidate.exists():
                print(f"\nUsing repaired reviews file: {cleaned_candidate}")
                source_file_path = cleaned_candidate
            else:
                print(
                    f"\nWARNING: cleaned reviews file not found at "
                    f"{cleaned_candidate}, loading raw (unrepaired) file instead"
                )

        print(f"Loading {source_file_path.name} → {table_name}")

        # Basic file validation
        if not source_file_path.is_file():
            print(f"  SKIPPED: {source_file_path} is not a valid file.")
            failed_files.append(source_file_path.name)
            continue

        if source_file_path.stat().st_size == 0:
            print(f"  SKIPPED: {source_file_path.name} is empty.")
            failed_files.append(source_file_path.name)
            continue

        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,
            autodetect=True,
            write_disposition="WRITE_TRUNCATE",
            allow_quoted_newlines=True,
            max_bad_records=10,
        )

        try:
            with source_file_path.open("rb") as source_file:
                job = client.load_table_from_file(
                    source_file,
                    table_id,
                    job_config=job_config,
                )

            job.result()

            print(f"  {table_name} loaded successfully.")

        except Exception as e:
            print(f"  {table_name} FAILED: {e}")
            failed_files.append(source_file_path.name)
            continue

    print("\n==============================")
    print("BigQuery ingestion completed.")
    print("==============================")

    if failed_files:
        print(
            f"Failed files ({len(failed_files)}): "
            f"{failed_files}"
        )

        # Fail the Airflow task if any file failed.
        raise RuntimeError(
            f"BigQuery ingestion failed for: {failed_files}"
        )

    print("All CSV files loaded successfully.")


def main():
    load_csvs_to_bigquery()


if __name__ == "__main__":
    main()