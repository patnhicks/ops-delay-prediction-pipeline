# Operational Logistics Intelligence Platform

A production-style, end-to-end data engineering and analytics pipeline
that ingests, processes, and analyzes US flight operations data to
support executive-level decision making on delay mitigation and
operational performance.

## Business Problem

Flight delays cost the US aviation industry billions annually and
create cascading operational failures across carriers, airports, and
routes. This platform provides operations directors with data-driven
visibility into delay patterns, root causes, and predictive risk —
enabling proactive rather than reactive decision making.

**Unit of analysis:** Individual flight  
**Target variable:** Arrival delay > 15 minutes (binary)  
**Prediction timing:** Prior to take-off  
**Decision maker:** Operations director / logistics leadership

## Architecture

Raw DOT Data → Ingestion Pipeline → ETL Processing →
Analytical Database → Predictive Models → Executive Dashboard

## Data Source

- **Source:** US Department of Transportation Bureau of
  Transportation Statistics
- **Dataset:** On-Time Reporting Carrier On-Time Performance
- **Time Frame:** January 2019 – December 2024
- **Scale:** 38.7 million flight records across 72 months
- **Carriers:** 18 US domestic carriers
- **Format:** Raw ZIP/CSV → Processed Parquet → MySQL

## Tech Stack

**Languages:** Python, SQL  
**Libraries:** pandas, NumPy, scikit-learn, matplotlib, seaborn  
**Database:** MySQL  
**Cloud:** AWS  
**Infrastructure:** Docker  
**Dashboard:** R Shiny / Python Dash  
**Version Control:** Git

## Project Structure

    ops-delay-prediction-pipeline/
    ├── data/
    │   ├── raw/          # Downloaded DOT zip files
    │   └── processed/    # Cleaned parquet files
    ├── ingestion/
    │   └── dot_pipeline.py    # Automated DOT data downloader
    ├── etl/
    │   └── transform.py       # Extract, transform, load pipeline
    ├── notebooks/
    │   └── 01_eda.ipynb       # Exploratory data analysis
    ├── models/                # Delay prediction models
    ├── dashboard/             # Executive dashboard
    ├── src/                   # Reusable utility functions
    ├── reports/               # Generated visualizations
    ├── requirements.txt
    └── README.md

## Key Findings (EDA)

Analysis of 38.7M flight records from 2019-2024 reveals:

**Systemic delay drivers:**

- Late aircraft cascades account for 38.3% of all delay minutes
  — the largest single cause
- Carrier-controllable issues (maintenance, crew) account for
  36.4% of delays
- Weather accounts for only 5.8% of delays despite being the
  most cited cause by passengers

**COVID impact:**

- 2020 flight volume collapsed 37% (7.4M → 4.7M flights)
- Average arrival delay went negative (-4.68 min) in 2020 due
  to reduced congestion
- Post-pandemic delay rates (2022-2024) are consistently worse
  than pre-pandemic at 20%+ vs 18.7%

**Carrier performance:**

- JetBlue (B6) has the worst delay rate at 26% among major carriers
- Delta (DL) is the best major carrier at 14.4% delay rate
- Southwest operates the highest volume (7.5M flights) while
  maintaining an 18.9% delay rate

**Geographic patterns:**

- Florida airports dominate worst performers — FLL, MIA, MCO
  all above 22% delay rate
- Hawaiian airports are the best performers — KOA and LIH below
  13.5% delay rate
- Chicago appears twice in worst 15 (ORD and MDW) indicating
  chronic airspace congestion

**Seasonal patterns:**

- Summer (June-August) consistently shows highest delay rates
- Fall (September-October) is the best operational window
- Pattern holds across all years except 2020

## Current Status

## Current Status

| Component                 | Status         |
| ------------------------- | -------------- |
| Data Ingestion            | ✅ Complete    |
| ETL Pipeline              | ✅ Complete    |
| Exploratory Data Analysis | ✅ Complete    |
| Database Layer (MySQL)    | ✅ Complete    |
| Predictive Modeling       | 🔄 In Progress |
| Executive Dashboard       | 📋 Planned     |
| Docker Containerization   | 📋 Planned     |
| AWS Deployment            | 📋 Planned     |

## How to Run

### Prerequisites

- Python 3.11+
- MySQL
- Docker (optional)

### Setup

```bash
# Clone the repository
git clone https://github.com/patnhicks/ops-delay-prediction-pipeline
cd ops-delay-prediction-pipeline

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

### Run the Pipeline

```bash
# Download raw data (2019-2024)
python ingestion/dot_pipeline.py

# Process and clean data
python etl/transform.py
```

## Author

**Patrick N. Hicks**  
MS Data Science, Texas Tech University (May 2026)  
[LinkedIn](https://linkedin.com/in/patnhicks) |
[GitHub](https://github.com/patnhicks)
