# from google.cloud import bigquery
# import os

# # Path to your service account key
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials/service-account.json"

# # Create BigQuery client
# client = bigquery.Client()

# print(" Connected successfully!")

# # List datasets
# for dataset in client.list_datasets():
#     print(dataset.dataset_id)

# biig query table name inspection
# import os
# from google.cloud import bigquery

# CREDENTIALS = "credentials/service-account.json"
# PROJECT_ID = "bigquery-data-pipeline-504708"
# DATASET_ID = "raw_sales"

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS

# client = bigquery.Client(project=PROJECT_ID)

# dataset_ref = client.dataset(DATASET_ID)

# tables = list(client.list_tables(dataset_ref))

# if not tables:
#     print("❌ No tables found.")
# else:
#     print(f"✅ Tables in {PROJECT_ID}.{DATASET_ID}:\n")

#     for table in tables:
#         print(f"- {table.table_id}")


# table inspection code
import os
from google.cloud import bigquery

CREDENTIALS = "credentials/service-account.json"
PROJECT_ID = "bigquery-data-pipeline-504708"
DATASET_ID = "raw_sales"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS

client = bigquery.Client(project=PROJECT_ID)

tables = list(client.list_tables(DATASET_ID))

if not tables:
    print(" No tables found.")
    raise SystemExit(1)

for table in sorted(tables, key=lambda x: x.table_id):
    print("\n" + "=" * 70)
    print(f"TABLE: {table.table_id}")
    print("=" * 70)

    table_ref = client.dataset(DATASET_ID).table(table.table_id)
    table_obj = client.get_table(table_ref)

    for field in table_obj.schema:
        print(f"{field.name:<45} {field.field_type:<15} {field.mode}")