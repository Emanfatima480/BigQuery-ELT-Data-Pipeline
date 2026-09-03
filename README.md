#  Olist E-Commerce Data Engineering Pipeline

An end-to-end data engineering pipeline that transforms raw Brazilian e-commerce data into a structured, analytics-ready data warehouse using **Python, Google BigQuery, dbt, Apache Airflow, and Docker**.

---

## 📌 Project Overview

This project implements a complete data engineering pipeline using the **Brazilian E-Commerce Public Dataset by Olist**, containing information about customers, orders, products, sellers, payments, reviews, and deliveries.

The pipeline takes raw CSV data, handles data-quality issues, loads the data into **Google BigQuery**, transforms it using **dbt**, and orchestrates the workflow with **Apache Airflow** running in Docker.

The final result is a dimensional data warehouse containing **staging models, fact tables, dimension tables, and analytical marts** that can be used for business intelligence and analytics.

---

##  Project Purpose

The purpose of this project is to demonstrate how raw e-commerce data can be transformed into a **reliable, structured, and analytics-ready data warehouse through an automated data engineering pipeline**.

The project automates the major stages of a modern data engineering workflow:

* Data quality and file repair
* Data ingestion
* Cloud data warehousing
* Data transformation
* Dimensional modeling
* Data quality testing
* Workflow orchestration

---

## 🏗️ Architecture

```text
                 Olist E-Commerce Dataset
                           │
                           ▼
                  ┌─────────────────┐
                  │   Raw CSV Files │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Python          │
                  │ Validation /    │
                  │ Repair          │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Python          │
                  │ BigQuery        │
                  │ Ingestion       │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Google BigQuery │
                  │   raw_sales     │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ dbt Staging     │
                  │ Models          │
                  └────────┬────────┘
                           │
                           ▼
              ┌───────────────────────────┐
              │ dbt Data Warehouse        │
              │                           │
              │ Dimensions + Facts +      │
              │ Analytical Marts          │
              └────────────┬──────────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Analytics-Ready │
                  │ BigQuery Tables │
                  └─────────────────┘

             Apache Airflow + Docker
                 orchestrate the
                    workflow
```

---

## 🔄 Data Pipeline

### 1. Data Quality & File Repair

The Olist dataset contains approximately **100,000 orders**.

During ingestion, the order reviews CSV was found to contain malformed records. A dedicated Python script was created to identify and repair problematic rows before loading the data.

**Review dataset:**

* Original rows: **104,719**
* Repaired/cleaned rows: **99,224**

Script:

```text
scripts/repair_reviews.py
```

This demonstrates handling real-world data quality problems instead of assuming that source files are always clean.

---

### 2. BigQuery Ingestion

Python scripts load the processed CSV files into **Google BigQuery**.

Raw data is stored in the:

```text
raw_sales
```

dataset.

Example source-to-table mapping:

```text
olist_orders_dataset.csv
        ↓
raw_sales.olist_orders
```

The ingestion process handles the source files and loads them into their corresponding BigQuery tables.

---

### 3. dbt Transformation

The raw BigQuery data is transformed using **dbt**.

The project contains **19 dbt models**:

#### Staging

**9 staging models** perform initial cleaning, casting, and preparation of raw data.

#### Dimensions

* `dim_customers`
* `dim_products`
* `dim_sellers`
* `dim_date`

#### Fact Tables

* `fact_orders`
* `fact_order_items`

#### Analytical Marts

* `mart_sales_summary` — daily sales and revenue metrics
* `mart_customer_sales` — customer purchasing behavior
* `mart_product_sales` — product-level sales and performance
* `mart_delivery_performance` — delivery status and performance

---

## ⭐ Analytical Data Marts

The final marts provide analytics-ready datasets for answering business questions such as:

* How are sales changing over time?
* Which products generate the most revenue?
* Which customers contribute the most sales?
* How many orders are delivered late?
* What is the average delivery performance?
* Which product categories perform best?

This separates **data engineering and transformation logic** from downstream analytics.

---

## ⚙️ Apache Airflow Orchestration

Apache Airflow orchestrates the pipeline inside Docker.

The DAG follows this workflow:

```text
repair_reviews
      ↓
ingest_to_bigquery
      ↓
dbt_transform
```

### Airflow Tasks

**1. `repair_reviews`**

Runs the Python data repair process.

**2. `ingest_to_bigquery`**

Loads the processed datasets into BigQuery.

**3. `dbt_transform`**

Runs dbt transformations to build the staging models, dimensions, facts, and analytical marts.

This allows the entire pipeline to be executed as an automated workflow instead of running each step manually.

---

## 🧪 Data Quality Testing

Data quality was validated using **dbt tests**.

The project successfully completed:

**35 dbt data tests**

The tests help verify the reliability and integrity of the transformed warehouse data.

Final warehouse verification was also performed using BigQuery queries to check:

* Table creation
* Row counts
* Sales calculations
* Customer aggregations
* Product aggregations
* Delivery metrics

---

## 🐳 Docker

Docker is used to provide a consistent environment for the pipeline.

The Airflow environment runs through Docker Compose and includes the required Python and dbt dependencies.

Main configuration files:

```text
docker-compose.yml
dockerfile
```

---

## 📂 Project Structure

```text
.
├── airflow/
│   ├── dags/
│   │   └── olist_pipeline.py
│   └── plugins/
│
├── data/
│   └── Olist CSV files
│
├── olist_dbt/
│   ├── dbt_project.yml
│   ├── models/
│   │   ├── staging/
│   │   └── marts/
│   └── ...
│
├── scripts/
│   ├── inspection_bigquery.py
│   ├── load_to_bigquery.py
│   └── repair_reviews.py
│
├── docker-compose.yml
├── dockerfile
└── README.md
```

> Raw datasets, credentials, dbt profiles, generated files, and logs are excluded from version control.

---

## 🚀 Getting Started

### Prerequisites

Install:

* Python
* Docker & Docker Compose
* Google Cloud account
* Google BigQuery
* dbt
* Apache Airflow

### 1. Clone the Repository

```bash
git clone https://github.com/Emanfatima480/BigQuery-ELT-Data-Pipeline
cd BigQuery-ELT-Data-Pipeline
```

### 2. Add the Dataset

Download the **Brazilian E-Commerce Public Dataset by Olist** and place the CSV files inside:

```text
data/
```

The raw dataset is not included in this repository because of its size.

### 3. Configure Google Cloud

Create a Google Cloud project and enable the BigQuery API.

Create a service account with appropriate BigQuery permissions and place the credentials locally in:

```text
credentials/
```

The credentials directory is excluded from Git.

### 4. Start Airflow

Build and start the Docker environment:

```bash
docker compose up --build -d
```

Open Airflow:

```text
http://localhost:8080
```

Locate the:

```text
olist_pipeline
```

DAG and trigger it.

### 5. Verify dbt

dbt can also be run manually from the local environment:

```bash
cd olist_dbt

dbt debug
dbt run
dbt test
```

---

## 🔐 Security

The following files and directories are intentionally excluded from Git:

* Google Cloud credentials
* `.env` files
* dbt `profiles.yml`
* Raw datasets
* Generated/cleaned data
* Airflow logs
* dbt logs
* dbt target files
* Python virtual environments

This prevents credentials and unnecessary generated files from being committed to the repository.

---

## 🛠️ Technologies

| Technology          | Purpose                                      |
| ------------------- | -------------------------------------------- |
| **Python**          | Data ingestion, validation, and file repair  |
| **Google BigQuery** | Cloud data warehouse                         |
| **dbt**             | Data transformation and dimensional modeling |
| **Apache Airflow**  | Workflow orchestration                       |
| **Docker**          | Environment and service management           |
| **SQL**             | Data transformation and analytics            |
| **Git/GitHub**      | Version control                              |

---

## 📊 Final Results

The completed pipeline produces an analytics-ready BigQuery warehouse containing:

* **9 staging models**
* **4 dimension tables**
* **2 fact tables**
* **4 analytical marts**
* **19 dbt models**
* **35 passing dbt tests**

The final warehouse can support downstream dashboards, reporting, and business analysis.

---

## 💡 What This Project Demonstrates

This project demonstrates practical experience with:

* Building an end-to-end ETL/ELT pipeline
* Handling malformed real-world CSV data
* Loading data into a cloud data warehouse
* Designing dimensional data models
* Building fact and dimension tables
* Creating analytical data marts
* Writing SQL transformations
* Implementing data quality tests
* Orchestrating workflows with Airflow
* Containerizing data engineering tools with Docker
* Working with Google BigQuery
* Managing credentials and generated files securely

---

## 🔮 Future Improvements

Possible future improvements include:

* Add a BI dashboard using Looker Studio or Power BI
* Add incremental dbt models
* Add pipeline monitoring and alerting
* Add automated CI/CD testing
* Add partitioning and clustering optimization in BigQuery
* Add more analytical marts and business metrics

---

## 👩‍💻 Author

**Eman Fatima**

BS Software Engineering | Aspiring Data Engineer

---

⭐ If you found this project useful, feel free to explore the repository and the pipeline implementation.
