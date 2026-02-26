# 🚀 Scalable ETL Pipeline on AWS Using Apache Spark & Athena

This project demonstrates the design and implementation of a fully automated, scalable ETL pipeline built on AWS.  

The pipeline extracts job market data for **Data Engineer roles in Canada** from the Adzuna API, processes the data using Apache Spark on AWS Glue, stores it in a structured data lake on Amazon S3, and enables analytical querying using Amazon Athena.

The workflow is fully orchestrated using AWS Step Functions and triggered automatically on a daily schedule using Amazon EventBridge.

---

## 🏗️ Architecture Overview


![ETL Architecture](assets/23azuna.drawio.png)

---

## 🛠️ Technologies & Services Used

- Adzuna API (Job Market Data Source)
- AWS Lambda (Serverless Extraction & File Management)
- Amazon S3 (Data Lake Storage)
- AWS Glue (Serverless ETL)
- Apache Spark (Distributed Data Processing)
- AWS Step Functions (Workflow Orchestration)
- Amazon EventBridge (Scheduling)
- AWS IAM (Access Control & Security)
- AWS CloudWatch (Monitoring & Logging)
- Amazon Athena (Serverless SQL Query Engine)

---

## 📂 Repository Structure
```
adzuna-etl-project/
│
├── raw_data/
│   ├── to_process/
│   └── processed/
│
├── transformed_data/
│
├── assets/
│   23azuna.drawio.png
│
├── src/
│   ├── lambda/
│   │   extract_lambda.py
│   │   move_processed_lambda.py
│   │
│   ├── glue/
│   │   transform_job.py
│   │
│   ├── step_functions/
│   │   state_machine.json
│   │
│   └── athena/
│
├── iam/
│   lambda_policy.json
│   glue_policy.json
│   step_function_policy.json
│
└── README.md

---
```
## 🔄 ETL Workflow Details

### 1️⃣ Data Extraction
- AWS Lambda fetches job listings from the Adzuna API
- Filters for:
  - Data Engineer roles
  - Canada location
  - Jobs posted within last 2 days
- Stores raw JSON files in:
  `raw_data/to_process/`

### 2️⃣ Data Transformation
- AWS Glue job runs Apache Spark
- Performs:
  - Flattening nested JSON structure
  - Column selection & renaming
  - Timestamp casting
  - Deduplication by job_id
- Outputs data in optimized Parquet format to:
  `transformed_data/`

### 3️⃣ File Lifecycle Management
- A second Lambda function moves processed JSON files from:
  `raw_data/to_process/`
  → `raw_data/processed/`

### 4️⃣ Query & Analytics
- Amazon Athena queries Parquet files directly from S3
- Enables serverless SQL-based analytics
## 🛡️ License

This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and share this project with proper attribution.

## About Me
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/mohamed-yasser-5a56672ab/i)
