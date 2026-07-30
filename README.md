# 📊 N100 Financial Intelligence

## 🌐 Live Demo

https://n100-financial-intelligence-tnkkhqyvgwljdtvfm8reuh.streamlit.app/

## 📂 GitHub Repository

https://github.com/Arunmozhi1997/N100-Financial-Intelligence

A comprehensive financial analytics platform for **Nifty 100 companies** built using **Python, SQLite, Streamlit, and Plotly**. The project performs ETL, financial ratio analysis, valuation, peer comparison, stock screening, and interactive dashboard visualization.

---

# 🚀 Features

- ETL pipeline for loading and cleaning financial statement data
- SQLite database for structured financial storage
- Financial Ratio & KPI calculations
- CAGR and Cash Flow analysis
- Valuation analysis
- Interactive 8-page Streamlit dashboard
- Financial Screener with CSV export
- Peer Comparison with Radar Charts
- Trend Analysis with Year-over-Year Growth
- Capital Allocation Treemap
- Annual Report Explorer
- Automated unit testing using Pytest

---

# 🛠 Tech Stack

- Python 3.11
- Pandas
- NumPy
- SQLite
- Streamlit
- Plotly
- OpenPyXL
- Pytest
- Ruff
- Black

---

# 📂 Project Structure

```
N100-Financial-Intelligence
│
├── db/
│   └── nifty100.db
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
│   │   ├── app.py
│   │   ├── pages/
│   │   └── utils/
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

# ⚙ Installation

Clone the repository

```bash
git clone <repository-url>
cd N100-Financial-Intelligence
```

Create virtual environment

```bash
python -m venv venv
```

Activate virtual environment

### Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶ Run ETL

```bash
python -m src.etl.loader
```

---

# 📈 Run Financial Ratio Engine

```bash
python -m src.analytics.ratio_engine
```

---

# 🔎 Run Stock Screener

```bash
python -m src.screener.engine
```

---

# 💻 Run Streamlit Dashboard

```bash
streamlit run src/dashboard/app.py
```

Dashboard URL

```text
http://localhost:8501
```

---

# 📊 Dashboard Pages

## 🏠 1. Home

- Nifty 100 market overview
- KPI cards
- Sector distribution
- Top-performing companies

---

## 🏢 2. Company Profile

- Company overview
- Financial KPIs
- Revenue & Net Profit trends
- ROE Trend
- Debt Trend
- Financial Ratios
- Profit & Loss
- Pros & Cons

---

## 🔎 3. Financial Screener

- Multi-factor screening
- Financial filters
- Live results
- CSV export

---

## 🤝 4. Peer Comparison

- Company vs Peer analysis
- Radar Chart
- Financial comparison table

---

## 📈 5. Trend Analysis

- Historical financial trends
- Multi-metric comparison
- Year-over-Year Growth
- Interactive line charts

---

## 🏦 6. Capital Allocation Map

- Interactive Treemap
- Capital allocation patterns
- Pattern-wise company analysis

---

## 💰 7. Valuation

- Valuation metrics
- Discount/Premium analysis
- Financial multiples
- Company valuation summary

---

## 📄 8. Annual Reports

- Search reports by company
- Search reports by year
- Report availability
- Report summary
- Report download links

---

# 📸 Dashboard Screenshots

> Save screenshots inside:

```
docs/screenshots/
```

### Home

```markdown
![Home](docs/screenshots/home.png)
```

### Company Profile

```markdown
![Profile](docs/screenshots/profile.png)
```

### Financial Screener

```markdown
![Screener](docs/screenshots/screener.png)
```

### Peer Comparison

```markdown
![Peers](docs/screenshots/peers.png)
```

### Trend Analysis

```markdown
![Trends](docs/screenshots/trends.png)
```

### Capital Allocation

```markdown
![Capital](docs/screenshots/capital.png)
```

### Valuation

```markdown
![Valuation](docs/screenshots/valuation.png)
```

### Annual Reports

```markdown
![Reports](docs/screenshots/reports.png)
```

---

# 🧪 Testing

Run all tests

```bash
pytest
```

Current Status

- ✅ 61/61 Unit Tests Passed
- ✅ Ruff Checks Passed
- ✅ Black Formatting Passed

---

# 📄 Generated Reports

The project automatically generates

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

- 92 Nifty 100 companies analyzed
- Interactive 8-page Streamlit dashboard
- SQLite financial database
- Financial ratio engine
- Valuation analysis
- Peer comparison
- Trend analysis
- Capital allocation visualization
- Annual report explorer
- CSV & Excel export
- 61/61 automated tests passed

---

# 🔮 Future Improvements

- Portfolio tracking
- Watchlist functionality
- AI-powered financial insights
- Real-time stock price integration
- Cloud deployment (AWS/Azure)
- User authentication

---

# 👨‍💻 Author

**Arunmozhi M**

**Data Analyst | Python | SQL | Financial Analytics | Streamlit | Machine Learning**

LinkedIn: *(https://www.linkedin.com/in/arunmozhi-muthu-65a29037b/)*

GitHub: *(https://github.com/Arunmozhi1997/N100-Financial-Intelligence)*
