# 📊 N100 Financial Intelligence

<<<<<<< HEAD
## 🌐 Live Demo

https://n100-financial-intelligence-tnkkhqyvgwljdtvfm8reuh.streamlit.app/

## 📂 GitHub Repository

https://github.com/Arunmozhi1997/N100-Financial-Intelligence

A comprehensive financial analytics platform for **Nifty 100 companies** built using **Python, SQLite, Streamlit, and Plotly**. The project performs ETL, financial ratio analysis, valuation, peer comparison, stock screening, and interactive dashboard visualization.
=======
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Live-red)
![SQLite](https://img.shields.io/badge/Database-SQLite-green)
![Tests](https://img.shields.io/badge/Tests-61%2F61-success)

A comprehensive Financial Analytics Platform for **Nifty 100 companies** built using **Python, SQLite, Streamlit, and Plotly**. The project performs ETL, financial ratio analysis, valuation, peer comparison, stock screening, and interactive dashboard visualization.


---

# 🚀 Live Demo

🌐 **https://n100-financial-intelligence-tnkkhqyvgwljdtvfm8reuh.streamlit.app/**

# 📂 GitHub Repository

https://github.com/Arunmozhi1997/N100-Financial-Intelligence

---

# 📑 Table of Contents

- Overview
- Features
- Tech Stack
- Project Architecture
- Dataset
- Project Structure
- Installation
- Usage
- Dashboard Pages
- Screenshots
- Testing
- Generated Reports
- Stock Screeners
- Project Highlights
- Skills Demonstrated
- Future Improvements
- Author

---

# 📌 Overview

N100 Financial Intelligence is an end-to-end financial analytics platform developed for Nifty 100 companies.

The application automates:

- Financial data processing
- Financial ratio calculation
- Company profiling
- Stock screening
- Peer comparison
- Trend analysis
- Capital allocation visualization
- Annual report exploration

The final output is an interactive Streamlit dashboard deployed online.

---

# ✨ Features

## 🔄 ETL Pipeline

- Data ingestion
- Data cleaning
- Data validation
- SQLite database loading

## 📈 Financial Analytics

- Financial Ratios
- CAGR
- Cash Flow Analysis
- Valuation Analysis
- Growth Analysis

## 🔎 Financial Screener

- Multi-factor screening
- Financial filters
- CSV Export

## 🤝 Peer Comparison

- Radar Charts
- Company Comparison
- Financial Metric Comparison

## 📊 Interactive Dashboard

- Home Dashboard
- Company Profile
- Financial Screener
- Peer Comparison
- Trend Analysis
- Capital Allocation
- Valuation
- Annual Reports

---

# 🛠 Tech Stack

| Category | Technologies |
|----------|--------------|
| Language | Python 3.11 |
| Database | SQLite |
| Data Processing | Pandas, NumPy |
| Dashboard | Streamlit |
| Visualization | Plotly |
| Excel | OpenPyXL |
| Testing | Pytest |
| Code Quality | Ruff, Black |
| Version Control | Git & GitHub |

---

# 🏗 Project Architecture

```
Raw Financial Data
        │
        ▼
   ETL Pipeline
        │
        ▼
 SQLite Database
        │
        ▼
 Financial Analytics Engine
        │
        ▼
 Streamlit Dashboard
        │
        ▼
 Live Web Application
```

---

# 📊 Dataset

| Item | Value |
|------|-------|
| Companies | 92 |
| Market | Nifty 100 |
| Database | SQLite |
| Financial Statements | Profit & Loss, Balance Sheet, Cash Flow |
| Years | Multi-year Financial Data |

---

# 📂 Project Structure

```
N100-Financial-Intelligence
│
├── db/
│   ├── nifty100.db
│   ├── schema.sql
│   └── exploratory_queries.sql
│
├── output/
│   ├── valuation_summary.xlsx
│   ├── valuation_flags.csv
│   ├── quality_compounder.xlsx
│   ├── value_pick.xlsx
│   ├── growth_accelerator.xlsx
│   ├── dividend_champion.xlsx
│   ├── debt_free_blue_chip.xlsx
│   ├── turnaround_watch.xlsx
│   └── screener_output.xlsx
│
├── src/
│   ├── analytics/
│   ├── dashboard/
│   ├── etl/
│   └── screener/
│
├── tests/
│
├── README.md
├── requirements.txt
└── pytest.ini
```

---

# ⚙ Installation

Clone the repository

```bash
git clone https://github.com/Arunmozhi1997/N100-Financial-Intelligence.git
```

Go inside

```bash
cd N100-Financial-Intelligence
```

Create virtual environment

```bash
python -m venv venv
```

Activate

### Windows

```bash
venv\Scripts\activate
```

Install packages

```bash
pip install -r requirements.txt
```

---

# ▶ Usage

## Run ETL

```bash
python -m src.etl.loader
```

## Run Financial Ratio Engine

```bash
python -m src.analytics.ratio_engine
```

## Run Stock Screener

```bash
python -m src.screener.engine
```

## Run Dashboard

```bash
streamlit run src/dashboard/app.py
```

Open

```
http://localhost:8501
```

---

# 📊 Dashboard Pages

## 🏠 Home

- Market Overview
- KPI Cards
- Sector Distribution
- Top Companies

---

## 🏢 Company Profile

- Company Overview
- Financial KPIs
- Revenue Trend
- Profit Trend
- Debt Trend
- Financial Ratios
- Pros & Cons

---

## 🔎 Financial Screener

- Multi-factor Filters
- Financial Screening
- CSV Export

---

## 🤝 Peer Comparison

- Company Comparison
- Radar Chart
- Financial Metrics

---

## 📈 Trend Analysis

- Historical Trends
- Year-over-Year Growth
- Interactive Charts

---

## 🏦 Capital Allocation

- Treemap Visualization
- Capital Distribution

---

## 💰 Valuation

- Valuation Metrics
- Discount/Premium Analysis
- Financial Multiples

---

## 📄 Annual Reports

- Search by Company
- Search by Year
- Report Availability

---

# 📸 Dashboard Screenshots

Create folder

```
docs/screenshots/
```

Add screenshots

```
home.png
profile.png
screener.png
peers.png
trends.png
capital.png
valuation.png
reports.png
```

Example

```markdown
## Home

![Home](docs/screenshots/home.png)
```

---

# 🧪 Testing

Run tests

```bash
pytest
```

## Test Status

✅ 61 / 61 Tests Passed

✅ Ruff Checks Passed

✅ Black Formatting Passed

---

# 📄 Generated Reports

Automatically generated reports

- valuation_summary.xlsx
- valuation_flags.csv
- quality_compounder.xlsx
- value_pick.xlsx
- growth_accelerator.xlsx
- dividend_champion.xlsx
- debt_free_blue_chip.xlsx
- turnaround_watch.xlsx
- screener_output.xlsx

---

# 📈 Stock Screeners

- Quality Compounder
- Value Pick
- Growth Accelerator
- Dividend Champion
- Debt Free Blue Chip
- Turnaround Watch

---

# 🏆 Project Highlights

- ✅ 92 Nifty 100 Companies
- ✅ SQLite Database
- ✅ ETL Pipeline
- ✅ Financial Ratio Engine
- ✅ Valuation Analysis
- ✅ Peer Comparison
- ✅ Financial Screener
- ✅ Trend Analysis
- ✅ Capital Allocation
- ✅ Annual Report Explorer
- ✅ Interactive 8-Page Dashboard
- ✅ Live Streamlit Deployment
- ✅ 61/61 Automated Tests Passed

---

# 💡 Skills Demonstrated

- ETL Development
- Data Cleaning
- Data Validation
- SQL
- SQLite
- Financial Analytics
- Data Visualization
- Streamlit
- Plotly
- Python
- Git & GitHub
- Software Testing
- Dashboard Development

---

# 🔮 Future Improvements

- Portfolio Tracker
- User Authentication
- Real-Time Stock Prices
- AI Financial Insights
- Portfolio Optimization
- Docker Deployment
- CI/CD Pipeline

---

# 👨‍💻 Author

## Arunmozhi M

**Data Analyst | Python | SQL | Financial Analytics | Streamlit | Machine Learning**

### 🌐 LinkedIn

<<<<<<< HEAD
GitHub: *(https://github.com/Arunmozhi1997/N100-Financial-Intelligence)*
=======
https://www.linkedin.com/in/arunmozhi-muthu-65a29037b/

### 💻 GitHub

https://github.com/Arunmozhi1997

---

# ⭐ Support

If you found this project useful, please consider giving it a ⭐ on GitHub.

It helps others discover the project and motivates future improvements.

