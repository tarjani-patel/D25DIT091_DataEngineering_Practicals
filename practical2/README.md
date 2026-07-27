# Practical 2: Automated Data Profiling and Data Quality Validation

## Problem Statement
Develop a data ingestion pipeline that interfaces with file-based, API-driven, and relational data sources. The system should generate synthetic customer data, profile incoming datasets, detect data quality issues, simulate schema drift, validate configuration files, and store validated records in a relational database.

---

## Objectives

- Generate synthetic customer profile data using Faker.
- Perform data profiling on incoming datasets.
- Detect data quality issues such as null values, invalid formats, missing primary keys, and duplicate records.
- Simulate schema drift in API responses.
- Validate configuration files.
- Store processed records in a SQLite database.
- Generate execution logs for validation results.

---

## Technology Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.x |
| Data Generation | Faker |
| Data Analysis | Pandas |
| Database | SQLite |
| API Data Format | JSON |
| Logging | Python Logging Module |

---

## Project Structure

```
Practical_2_Data_Profiling/
│
├── Practical2.ipynb
├── customer_data.csv
├── transactions.json
├── config.txt
├── customer.db
├── validation.log
└── README.md
```

---

## Workflow

```
Generate Customer Data
        │
        ▼
Data Profiling
        │
        ▼
Inject Data Quality Issues
        │
        ▼
Validate Dataset
        │
        ▼
Generate Nested API Logs
        │
        ▼
Simulate Schema Drift
        │
        ▼
Validate Configuration File
        │
        ▼
Store Data in SQLite
        │
        ▼
Generate Validation Logs
```

---

## Files Generated

### customer_data.csv
Contains 100 synthetic customer records generated using the Faker library.

### transactions.json
Contains nested API transaction logs representing semi-structured data.

### config.txt
Configuration file containing intentional validation errors.

### customer.db
SQLite database containing validated customer records.

### validation.log
Execution log recording data quality validation results.

---

## Data Quality Checks Implemented

- Missing Primary Key Detection
- Missing Value Detection
- Email Format Validation
- Phone Number Validation
- Duplicate Record Detection
- Configuration File Validation
- Schema Drift Detection

---

## Expected Output

- Customer dataset generated successfully.
- Invalid records identified.
- Nested JSON API logs created.
- Schema drift detected successfully.
- Configuration errors identified.
- Data stored in SQLite database.
- Validation log generated.

---

## Learning Outcome

This practical demonstrates the implementation of an end-to-end data ingestion and validation pipeline. It covers synthetic data generation, data profiling, schema drift detection, validation of structured and semi-structured data, relational database storage, and automated execution logging using Python.

---

## Author

**Name:** Tarjani Patel

**Course:** B.Tech – Information Technology

**Subject:** Data Engineering Laboratory