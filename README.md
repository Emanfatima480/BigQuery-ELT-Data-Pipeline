# 🚀 Olist E-Commerce Data Engineering Pipeline

An end-to-end data engineering pipeline that transforms raw Brazilian e-commerce data into a structured, analytics-ready data warehouse using **Python, Google BigQuery, dbt, Apache Airflow, and Docker**.

---

## 📌 Project Overview

This project implements a complete data pipeline using the **Brazilian E-Commerce Public Dataset by Olist**, which contains information about customers, orders, products, sellers, payments, reviews, and deliveries.

The pipeline takes raw CSV data, handles data-quality issues, loads the data into **Google BigQuery**, transforms it using **dbt**, and orchestrates the entire workflow with **Apache Airflow** running in Docker.

The final result is a dimensional data warehouse containing staging models, fact tables, dimension tables, and analytical marts that can be used for business intelligence and analytics.

---

## 🎯 Project Purpose

The purpose of this project is to demonstrate how raw e-commerce data can be transformed into a **reliable, structured, and analytics-ready data warehouse through an automated data engineering pipeline**.

Instead of manually processing individual CSV files, the pipeline automates the major stages of the data engineering workflow:
* Data quality and file repair
* Data ingestion
* Cloud data warehousing
* Data transformation
* Dimensional modeling
* Data quality testing
* Workflow orchestration

---

## 📂 Repository Structure

```text
.
├── airflow/
│   ├── dags/
│   │   └── olist_pipeline.py    # Main Airflow DAG orchestrating the pipeline
│   └── plugins/
├── data/                        # Local raw data storage (Git ignored except structure)
│   ├── olist_customers_dataset.csv
│   └── ... (other Olist source CSVs)
├── olist_dbt/                   # dbt transformation layer
│   ├── dbt_project.yml
│   ├── profiles.yml             # dbt connection profiles
│   ├── models/
│   │   ├── marts/               # Final analytics tables
│   │   └── staging/             # Raw views/clean ups
│   └── ...
├── scripts/                     # Python scripts called by Airflow / Local setup
│   ├── inspection_bigquery.py
│   ├── load_to_bigquery.py
│   └── repair_reviews.py
├── docker-compose.yml           # Local Airflow deployment definition
└── dockerfile                   # Custom Airflow image with dbt/Python dependencies
```

---

## 🏗️ Architecture

```text
                    Olist E-Commerce Dataset
                              │
                              ▼
                    ┌───────────────────┐
                    │   Raw CSV Files   │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ Python Data       │
                    │ Validation/Repair │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ Python Ingestion  │
                    │ → BigQuery        │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ BigQuery          │
                    │ raw_sales         │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ dbt Staging       │
                    │ Models            │
                    └─────────┬─────────┘
                              │
                              ▼
              ┌───────────────────────────────┐
              │ dbt Data Warehouse Models     │
              │                               │
              │ Dimensions + Facts + Marts    │
              └───────────────┬───────────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ Analytics-Ready   │
                    │ BigQuery Tables   │
                    └───────────────────┘

             Apache Airflow + Docker
             orchestrate the pipeline
```

---

## 🔄 Data Pipeline Stages

### 1. Raw Data & Quality Repair
The project uses the Olist Brazilian E-Commerce dataset (~100,000 orders). The order reviews dataset contained malformed CSV records. A dedicated Python repair process (`scripts/repair_reviews.py`) identifies and reconstructs problematic rows before loading:
* **Original rows:** 104,719
* **Cleaned rows:** 99,224

*(Note: Raw CSV files are excluded from GitHub tracking via `.gitignore` due to size).*

### 2. BigQuery Ingestion
Python scripts load the cleaned CSV datasets into Google BigQuery under the `raw_sales` dataset, mapping source files directly to their respective staging landing tables (e.g., `olist_orders_dataset.csv` → `raw_sales.olist_orders`).

### 3. dbt Transformation & Dimensional Modeling
dbt transforms the raw BigQuery data into **19 distinct models**:
* **9 staging models**: Basic cleaning and casting.
* **4 dimension models** (`dim_customers`, `dim_products`, `dim_sellers`, `dim_date`).
* **2 fact models** (`fact_orders`, `fact_order_items`).
* **4 analytical mart models**:
  * `mart_sales_summary`: Daily aggregated sales metrics.
  * `mart_customer_sales`: Customer lifetime purchasing behavior.
  * `mart_product_sales`: Product-level revenue and performance metrics.
  * `mart_delivery_performance`: Tracks order fulfillment status (*On Time, Late, Not Delivered*).

---

## ⚙️ Airflow Orchestration

Apache Airflow orchestrates the pipeline execution inside Docker containers using the following DAG structure:

```text
repair_reviews ──> ingest_to_bigquery ──> dbt_transform
```
* **Task 1 (`repair_reviews`)**: Executes the Python data parsing script.
* **Task 2 (`ingest_to_bigquery`)**: Loads repaired CSV data to Google BigQuery.
* **Task 3 (`dbt_transform`)**: Runs dbt compilation, builds the analytical warehouse, and triggers data testing.

---

## 🚀 Getting Started & Setup

### Prerequisites
* [Docker & Docker Compose](https://docker.com) installed locally.
* A [Google Cloud Project](https://google.com) with **BigQuery API** enabled.
* A GCP Service Account JSON key with **BigQuery Admin** permissions.

### 1. Environment & Credentials Setup
1. Clone this repository:
   ```bash
   git clone https://github.com
   cd your-repo-name
   ```
2. Place your GCP Service Account JSON key inside a local directory named `credentials/` (this is ignored by Git for security) and name it `google_creds.json`.
3. Download the Olist dataset from Kaggle and place the raw CSV files inside the `data/` directory matching the tree structure above.

### 2. Launching the Pipeline
1. Build and start the Airflow multi-container environment:
   ```bash
   docker compose up --build -d
   ```
2. Access the Airflow Web UI at `http://localhost:8080` (Default credentials: `airflow` / `airflow`).
3. Locate the `olist_pipeline` DAG, unpause it, and trigger the execution.

### 3. Running dbt Manually (Optional)
If you want to run transformations manually outside of Airflow using your local environment:
```bash
cd olist_dbt
dbt debug  # Verify connection to BigQuery
dbt run    # Run transformations
dbt test   # Run data assertions
```
