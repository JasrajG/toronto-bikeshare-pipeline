# 🚲 Toronto Bike Share Real-Time Data Pipeline

## 📖 Project Overview
This project is an automated Data Engineering pipeline that takes real-time GBFS (General Bikeshare Feed Specification) data from Toronto Bike Share. It extracts live station statuses, transforms the data into a time-series format, and loads it into a cloud PostgreSQL data warehouse for analysis and visualization.

*Currently completed **Phase 1 (v1.0)** of a multi-phase project.*

## 🏗️ Architecture & Tech Stack
*   **Language:** Python (Pandas, Requests, SQLAlchemy)
*   **Data Warehouse:** PostgreSQL (Neon.tech serverless cloud DB)
*   **Visualization:** Folium (Python mapping library)
*   **API:** Toronto Public Bike Share GBFS v3.0

## ⚙️ The ETL Pipeline
The pipeline (`etl_pipeline.py`) is has three distinct steps:
1.  **Extract:** Dynamically parses the GBFS v3.0 discovery endpoint to locate the `station_information` and `station_status` feeds, pulling the JSON payloads via HTTP GET requests.
2.  **Transform:** Flattens nested JSON structures into Pandas DataFrames, performs an inner join on `station_id`, and append a processing timestamp to enable time-series tracking.
3.  **Load:** Connects to a cloud PostgreSQL database securely via environment variables and appends the batch data to the `bike_station_status` table.

## 📊 Data Model (Schema)
The data is stored in Postgres with the following schema to support time-series analysis:

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `station_id` | Text | Unique identifier for the bike station |
| `name` | Text | Human-readable name of the station |
| `lat` | Float | Latitude coordinate |
| `lon` | Float | Longitude coordinate |
| `num_vehicles_available` | Integer | Real-time count of bikes at the station |
| `last_updated` | Timestamp | Processing time of the pipeline run |



## 🚀 Next Steps (Phase 2)
*   Automate the pipeline execution using GitHub Actions or Cron to run every 5 minutes.
*   Add visualtization
*   (Phase 3) Build a real-time Streamlit dashboard to simulate predicted bike movements based on live dock depletions.