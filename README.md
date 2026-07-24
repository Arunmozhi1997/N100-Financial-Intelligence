# N100 Financial Intelligence

## Overview

N100 Financial Intelligence is a Python-based financial analytics platform that processes financial statement data of Nifty 100 companies. The project performs ETL (Extract, Transform, Load), stores cleaned data in SQLite, calculates key financial ratios and KPIs, and generates stock screener reports based on predefined investment strategies.

---

## Features

- ETL pipeline for loading and cleaning financial data
- SQLite database for structured storage
- Financial ratio calculations
- CAGR (Compound Annual Growth Rate) analysis
- Cash Flow KPI analysis
- Six predefined stock screeners
- Combined Excel screener report
- Automated unit testing using Pytest

---

## Tech Stack

- Python 3.11
- Pandas
- NumPy
- SQLite
- OpenPyXL
- Pytest
- Ruff
- Black

---

## Project Structure

```
N100-Financial-Intelligence
│
├── db/
│   └── nifty100.db
│
├── output/
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
│   └── kpi/
│
├── README.md
├── requirements.txt
└── pytest.ini
```

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd N100-Financial-Intelligence
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

### Windows

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Run ETL

```bash
python -m src.etl.loader
```

---

## Run Financial Ratio Engine

```bash
python -m src.analytics.ratio_engine
```

---

## Run Stock Screener

```bash
python -m src.screener.engine
```

---

## Testing

Run all unit tests:

```bash
pytest
```

Current Status:

- **61/61 Tests Passed**
- Ruff: All checks passed
- Black: Code formatted

---

## Output Reports

The application generates the following reports:

- quality_compounder.xlsx
- value_pick.xlsx
- growth_accelerator.xlsx
- dividend_champion.xlsx
- debt_free_blue_chip.xlsx
- turnaround_watch.xlsx
- screener_output.xlsx

---

## Stock Screeners

The project includes six investment screeners:

- Quality Compounder
- Value Pick
- Growth Accelerator
- Dividend Champion
- Debt Free Blue Chip
- Turnaround Watch

---

## Future Improvements

- Interactive Streamlit dashboard
- Company comparison
- Financial charts
- Company search and filtering
- Portfolio analysis
- Cloud deployment

---

## Author

**Arunmozhi M**

Data Analyst | Python | SQL | Financial Analytics