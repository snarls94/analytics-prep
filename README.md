# CJIS Audit & Accountability Analytics

![Live Site](https://img.shields.io/badge/Live-Site-blue)](https://snarls94.github.io/analytics-prep/)
![Incident Alerts](https://github.com/snarls94/analytics-prep/actions/workflows/incident-alert.yml/badge.svg)

A local “embedded analytics” demonstration for CJIS Audit & Accountability (AU) controls. This repository implements a minimal end-to-end pipeline—data ingestion, validation, anomaly detection, weekly compliance reporting, and interactive dashboards—that maps directly to FBI CJIS Security Policy v6.0 AU requirements.

## Table of Contents

- [Project Overview](#project-overview)
- [AU Controls Covered](#au-controls-covered)
- [Data Sources](#data-sources)
- [Folder Structure](#folder-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [1. Ingest & Normalize Logs](#1-ingest--normalize-logs)
  - [2. Failure Detection & Recovery](#2-failure-detection--recovery)
  - [3. Weekly Review & Reporting](#3-weekly-review--reporting)
  - [4. Dashboard & Drill-downs](#4-dashboard--drill-downs)
- [Key Artifacts & Outputs](#key-artifacts--outputs)
- [Next Steps](#next-steps)
- [License](#license)
- [Contact](#contact)

## Project Overview

This project demonstrates how a 2–3-person embedded analytics team could implement CJIS AU requirements:

1. **ETL & Validation (AU-2 & AU-3):** Ingest raw audit-log files, enforce schema (event type, timestamp, user, outcome, source, etc.), and load into PostgreSQL.
2. **Failure Detection (AU-5):** Monitor the logging process, alert within 1 hour on failures, and auto-restart.
3. **Weekly Review & Reporting (AU-6 & AU-7):** Run a scheduled job to analyze weekly logs for anomalies, generate a PDF compliance report, and email to stakeholders.
4. **Dashboards & Drill-downs (AU-4, AU-8, AU-9, AU-11, AU-12):** Provide an interactive web dashboard to explore logs, retention metrics, and event summaries, secured and retained per policy.

## AU Controls Covered

- **AU-1**: Policy & Procedures documentation
- **AU-2**: Event logging definitions & collection
- **AU-3**: Content requirements for audit records
- **AU-4**: Storage capacity planning
- **AU-5**: Detection & recovery of logging failures
- **AU-6**: Review, analysis & reporting cadence
- **AU-7**: Audit-record reduction & summary reports
- **AU-8**: Timestamp precision & normalization
- **AU-9**: Protection of audit information
- **AU-11**: Retention policy (≥1 year)
- **AU-12**: Configurable log generation controls
- **Correlation**: Cross-repository log correlation

## Data Sources

- **Sample Audit Logs**: CSV exports simulating CJI access events
- **System Metadata**: JSON describing system components & user roles
- **Policy Reference**: Excerpts from CJIS Security Policy v6.0 (AU Sections)

## Folder Structure

├── data/
├── .github/
│ ├── ISSUE_TEMPLATE/
│ │ └── policy-review.yml
│ └── workflows/
│ ├── deploy-docs.yml
│ └── schedule-review.yml
├── docs/
│ ├── index.md
│ ├── purpose.md
│ ├── scope.md
│ ├── roles.md
│ └── review_cycle.md
├── mkdocs.yml
└── README.md # This document

│ ├── raw/ # Example audit_log CSVs
│ └── processed/ # Cleaned & validated logs
├── scripts/
│ ├── ingest_logs.py # ETL & schema enforcement
│ ├── monitor_logging.py # AU-5 failure detection & restart
│ ├── analyze_weekly.py # AU-6 log analysis & PDF report
│ └── anomaly_detection.py # AU-7 reduction & flagging
├── notebooks/
│ └── eda_audit.ipynb # Exploratory analysis & validation
├── dashboards/
│ └── cjis_dashboard.html # Interactive (Plotly/Kibana) export
├── airflow/
│ └── dag_cjis_au.py # DAG orchestration for ETL→monitor→report
├── reports/
│ └── weekly_compliance.pdf # Sample output
├── requirements.txt # Python dependencies

## Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL (or local Docker container)
- Git

### Installation

```bash
git clone https://github.com/your-username/cjis-audit-analytics.git
cd cjis-audit-analytics
python3 -m venv .venv
source .venv/bin/activate      # macOS/Linux
pip install -r requirements.txt

Configure your database connection in scripts/ingest_logs.py (set DATABASE_URL) and ensure data/raw/ contains at least one audit_log_*.csv.
Usage
1. Ingest & Normalize Logs
python scripts/ingest_logs.py \
  --input data/raw/audit_log.csv \
  --output data/processed/cleaned_logs.csv

Validates AU-2 & AU-3: ensures each record has event_type, timestamp, user_id, outcome, source, and system_name.
2. Failure Detection & Recovery
python scripts/monitor_logging.py

Simulates AU-5: watches audit_log.txt, alerts if no new entries within threshold, and restarts the logging process.
3. Weekly Review & Reporting
python scripts/analyze_weekly.py \
  --input data/processed/cleaned_logs.csv \
  --output reports/weekly_compliance.pdf

Implements AU-6 & AU-7: aggregates weekly metrics, flags anomalies, and generates a PDF report.
4. Dashboard & Drill-downs
Open dashboards/cjis_dashboard.html in your browser to interactively explore events, failure trends, retention timelines, and cross-system correlations (AU-4, AU-8, AU-9, AU-11, AU-12).
Key Artifacts & Outputs
PostgreSQL Table audit_logs with enforced schema

monitor_logging.py: real-time failure detection & auto-restart

weekly_compliance.pdf: scheduled compliance report

cjis_dashboard.html: interactive analytics dashboard

Next Steps
Integrate a real BI tool (Tableau/Looker) for richer dashboards
Add Alertmanager or Slack webhook integration for alerts
Automate retention (AU-11) via S3 lifecycle or SQL partition cleanup
Expand correlation across multiple log repositories
MkDocs Permissions – How to lock down editing with page‐level restrictions
GitHub Actions Scheduling – Using `on: schedule` and cron syntax
We now use a lightweight Python alert script (scripts/check_unauth_alert.py) scheduled via GitHub Actions (or cron) in place of ElastAlert for incident‐driven GitHub Issues.
Incident-Driven Alerts – GitHub Action on self-hosted runner polling Elasticsearch every 5 minutes and auto-creating issues for UNAUTHORIZED_ACCESS events.

License
MIT © Sruthi Narla

Contact
Sruthi Narla • sruthinarlas@gmail.com
GitHub: @snarls94
```
