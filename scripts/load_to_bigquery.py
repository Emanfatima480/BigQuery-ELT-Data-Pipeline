import os
from pathlib import Path
from google.cloud import bigquery

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials/service-account.json"

client = bigquery.Client()
PROJECT_ID = client.project
DATASET_ID = "raw_sales"
DATA_FOLDER = Path("data")

failed_files = []

for csv_file in DATA_FOLDER.glob("*.csv"):
    table_name = csv_file.stem.replace("_dataset", "")
    table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"

    print(f"Loading {csv_file.name} → {table_name}")

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        write_disposition="WRITE_TRUNCATE",
        allow_quoted_newlines=True,
        max_bad_records=10,
    )

    try:
        with open(csv_file, "rb") as source_file:
            job = client.load_table_from_file(source_file, table_id, job_config=job_config)
        job.result()
        print(f" {table_name} loaded successfully")
    except Exception as e:
        print(f"  {table_name} FAILED: {e}")
        failed_files.append(csv_file.name)
        continue  # move on to the next file instead of crashing

print("\nDone.")
if failed_files:
    print(f" {len(failed_files)} file(s) failed: {failed_files}")
else:
    print(" All CSV files loaded successfully!")