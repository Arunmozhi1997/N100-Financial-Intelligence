from pathlib import Path
import sqlite3

import pandas as pd
import logging

from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets,
    debt_to_equity,
    interest_coverage_ratio,
    asset_turnover,
)

from src.analytics.cashflow_kpis import (
    free_cash_flow,
    capex_intensity,
    fcf_conversion_rate,
)

# ==========================================
# Database Connection
# ==========================================

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "db" / "nifty100.db"

conn = sqlite3.connect(DB_PATH)

OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=OUTPUT_DIR / "ratio_edge_cases.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
)

logger = logging.getLogger(__name__)

# ==========================================
# Load Tables
# ==========================================

profit_df = pd.read_sql("SELECT * FROM profitandloss", conn)
balance_df = pd.read_sql("SELECT * FROM balancesheet", conn)
cashflow_df = pd.read_sql("SELECT * FROM cashflow", conn)

companies_df = pd.read_sql(
    "SELECT * FROM companies",
    conn,
)

print("\n" + "=" * 60)
print("COMPANIES")
print("=" * 60)

print("Shape :", companies_df.shape)

print("\nColumns")
print(companies_df.columns.tolist())

# ==========================================
# Normalize Merge Keys
# ==========================================

for df in [profit_df, balance_df, cashflow_df]:
    df["company_id"] = (
        df["company_id"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df.dropna(subset=["year"], inplace=True)
    df["year"] = df["year"].astype(int)

# ==========================================
# Basic Information
# ==========================================

print("=" * 60)
print("TABLE SHAPES")
print("=" * 60)

print("Profit & Loss :", profit_df.shape)
print("Balance Sheet :", balance_df.shape)
print("Cash Flow     :", cashflow_df.shape)

print("\n" + "=" * 60)
print("COLUMN NAMES")
print("=" * 60)

print("\nProfit & Loss")
print(profit_df.columns.tolist())

print("\nBalance Sheet")
print(balance_df.columns.tolist())

print("\nCash Flow")
print(cashflow_df.columns.tolist())

# ==========================================
# Data Types
# ==========================================

print("\n" + "=" * 60)
print("DATA TYPES")
print("=" * 60)

print("\nProfit")
print(profit_df[["company_id", "year"]].dtypes)

print("\nBalance")
print(balance_df[["company_id", "year"]].dtypes)

print("\nCashflow")
print(cashflow_df[["company_id", "year"]].dtypes)

# ==========================================
# Company Counts
# ==========================================

print("\n" + "=" * 60)
print("UNIQUE COMPANIES")
print("=" * 60)

print("Profit & Loss :", profit_df["company_id"].nunique())
print("Balance Sheet :", balance_df["company_id"].nunique())
print("Cash Flow     :", cashflow_df["company_id"].nunique())

# ==========================================
# Remove Duplicate Company-Year Records
# ==========================================

profit_df = profit_df.drop_duplicates(
    subset=["company_id", "year"],
    keep="first"
)

balance_df = balance_df.drop_duplicates(
    subset=["company_id", "year"],
    keep="first"
)

cashflow_df = cashflow_df.drop_duplicates(
    subset=["company_id", "year"],
    keep="first"
)

print("\nAfter Removing Duplicates")
print("Profit :", profit_df.shape)
print("Balance:", balance_df.shape)
print("Cashflow:", cashflow_df.shape)

# ==========================================
# Sample Data
# ==========================================

print("\n" + "=" * 60)
print("FIRST 10 RECORDS")
print("=" * 60)

print("\nProfit & Loss")
print(profit_df[["company_id", "year"]].head(10))

print("\nBalance Sheet")
print(balance_df[["company_id", "year"]].head(10))

print("\nCash Flow")
print(cashflow_df[["company_id", "year"]].head(10))

# ==========================================
# Check Specific Companies
# ==========================================

print("\n" + "=" * 60)
print("ABB")
print("=" * 60)

print("\nProfit")
print(profit_df[profit_df["company_id"] == "ABB"].head())

print("\nBalance")
print(balance_df[balance_df["company_id"] == "ABB"].head())

print("\nCashflow")
print(cashflow_df[cashflow_df["company_id"] == "ABB"].head())

print("\n" + "=" * 60)
print("TCS")
print("=" * 60)

print("\nProfit")
print(profit_df[profit_df["company_id"] == "TCS"].head())

print("\nBalance")
print(balance_df[balance_df["company_id"] == "TCS"].head())

print("\nCashflow")
print(cashflow_df[cashflow_df["company_id"] == "TCS"].head())

# ==========================================
# Merge Tables
# ==========================================

financial_df = (
    profit_df
    .merge(
        balance_df,
        on=["company_id", "year"],
        how="inner",
        suffixes=("_pl", "_bs"),
    )
    .merge(
        cashflow_df,
        on=["company_id", "year"],
        how="inner",
    )
)

# ==========================================
# Merge Company Master
# ==========================================

companies_df["id"] = (
    companies_df["id"]
    .astype(str)
    .str.strip()
    .str.upper()
)

financial_df = financial_df.merge(
    companies_df,
    left_on="company_id",
    right_on="id",
    how="left",
)

print("\nAfter Company Merge")
print(financial_df.shape)

# ==========================================
# Compute ROCE
# ==========================================

financial_df["computed_roce"] = (
    (
        financial_df["operating_profit"]
        + financial_df["other_income"]
    )
    /
    (
        financial_df["equity_capital"]
        + financial_df["reserves"]
        + financial_df["borrowings"]
    )
) * 100

financial_df["roce_difference"] = (
    financial_df["computed_roce"]
    - financial_df["roce_percentage"]
).abs()

anomalies = financial_df[
    financial_df["roce_difference"] > 5
]

print("\nROCE anomalies:", len(anomalies))

for _, row in anomalies.iterrows():
    logger.info(
        f"{row['company_id']} | "
        f"Year={row['year']} | "
        f"Computed={row['computed_roce']:.2f} | "
        f"Source={row['roce_percentage']} | "
        f"Difference={row['roce_difference']:.2f}"
    )


# ==========================================
# Compare ROE
# ==========================================

financial_df["computed_roe"] = (
    financial_df["net_profit"]
    /
    (
        financial_df["equity_capital"]
        + financial_df["reserves"]
    )
) * 100

financial_df["roe_difference"] = (
    financial_df["computed_roe"]
    - financial_df["roe_percentage"]
).abs()

roe_anomalies = financial_df[
    financial_df["roe_difference"] > 5
]

print("\nROE anomalies:", len(roe_anomalies))

for _, row in roe_anomalies.iterrows():
    logger.info(
        f"ROE | {row['company_id']} | "
        f"Year={row['year']} | "
        f"Computed={row['computed_roe']:.2f} | "
        f"Source={row['roe_percentage']} | "
        f"Difference={row['roe_difference']:.2f}"
    )

print("\nProfit duplicates:")
print(profit_df.duplicated(subset=["company_id", "year"]).sum())

print("\nBalance duplicates:")
print(balance_df.duplicated(subset=["company_id", "year"]).sum())

print("\nCashflow duplicates:")
print(cashflow_df.duplicated(subset=["company_id", "year"]).sum())

# ==========================================
# Calculate Financial Ratios
# ==========================================

results = []

for _, row in financial_df.iterrows():

    npm = net_profit_margin(
        row["net_profit"],
        row["sales"],
    )

    opm = operating_profit_margin(
        row["operating_profit"],
        row["sales"],
    )

    roe = return_on_equity(
        row["net_profit"],
        row["equity_capital"],
        row["reserves"],
    )

    roce = return_on_capital_employed(
        row["operating_profit"] + row["other_income"],
        row["equity_capital"],
        row["reserves"],
        row["borrowings"],
    )

    roa = return_on_assets(
        row["net_profit"],
        row["total_assets"],
    )

    debt_equity = debt_to_equity(
        row["borrowings"],
        row["equity_capital"],
        row["reserves"],
    )

    icr = interest_coverage_ratio(
        row["operating_profit"],
        row["other_income"],
        row["interest"],
    )

    asset_turn = asset_turnover(
        row["sales"],
        row["total_assets"],
    )

    fcf = free_cash_flow(
        row["operating_activity"],
        row["investing_activity"],
    )

    _, capex_category = capex_intensity(
        row["investing_activity"],
        row["sales"],
    )

    fcf_rate = fcf_conversion_rate(
        fcf,
        row["operating_profit"],
    )

    results.append({
    "company_id": row["company_id"],
    "year": row["year"],

    "net_profit_margin_pct": npm,
    "operating_profit_margin_pct": opm,
    "return_on_equity_pct": roe,

    "debt_to_equity": debt_equity,
    "interest_coverage": icr,
    "asset_turnover": asset_turn,

    "free_cash_flow_cr": fcf,

    "capex_cr": abs(row["investing_activity"]),

    "earnings_per_share": row["eps"],

    "book_value_per_share":
        (row["equity_capital"] + row["reserves"]) / row["equity_capital"]
        if row["equity_capital"] != 0 else None,

    "dividend_payout_ratio_pct": row["dividend_payout"],

    "total_debt_cr": row["borrowings"],

    "cash_from_operations_cr": row["operating_activity"],
})

ratio_df = pd.DataFrame(results)

print("\nRatio DataFrame")
print(ratio_df.head())
print(ratio_df.columns.tolist())

print("\nRows:", len(ratio_df))

# ==========================================
# Merge Result
# ==========================================

print("\n" + "=" * 60)
print("MERGED DATA")
print("=" * 60)

print("Shape :", financial_df.shape)

if financial_df.empty:
    print("\n❌ No matching rows found.")
else:
    print("\n✅ Merge Successful")
    print(financial_df.head())
# ==========================================
# Save Financial Ratios to SQLite
# ==========================================

cursor = conn.cursor()

# Remove old KPI records
cursor.execute("DELETE FROM financial_ratios")
conn.commit()

# Insert newly calculated KPIs
ratio_df.to_sql(
    "financial_ratios",
    conn,
    if_exists="append",
    index=False,
)

print("\n✅ Financial ratios saved successfully!")
print("Rows inserted:", len(ratio_df))

conn.commit()
conn.close()

