from pathlib import Path
import sqlite3
import yaml
import pandas as pd

# ==========================================
# Project Paths
# ==========================================

BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "db" / "nifty100.db"
CONFIG_PATH = BASE_DIR / "config" / "screener_config.yaml"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# ==========================================
# Database Connection
# ==========================================

conn = sqlite3.connect(DB_PATH)

# ==========================================
# Load Tables
# ==========================================

financial_df = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn,
)

financial_df["year"] = (
    pd.to_numeric(financial_df["year"], errors="coerce")
    .fillna(0)
    .astype(int)
)

companies_df = pd.read_sql(
    "SELECT * FROM companies",
    conn,
)

market_df = pd.read_sql(
    "SELECT * FROM market_cap",
    conn,
)

market_df["year"] = (
    pd.to_numeric(market_df["year"], errors="coerce")
    .fillna(0)
    .astype(int)
)

analysis_df = pd.read_sql(
    "SELECT * FROM analysis",
    conn,
)

profit_df = pd.read_sql(
    """
    SELECT
        company_id,
        year,
        sales
    FROM profitandloss
    """,
    conn,
)
profit_df["year"] = (
    pd.to_numeric(profit_df["year"], errors="coerce")
    .fillna(0)
    .astype(int)
)

# ==========================================
# Merge Company Information
# ==========================================

companies_df = companies_df.rename(
    columns={"id": "company_id"}
)

financial_df = financial_df.merge(
    companies_df,
    on="company_id",
    how="left",
)

analysis_df = analysis_df.drop_duplicates(subset=["company_id"])

print("\nAfter Company Merge")
print(financial_df.shape)

financial_df = financial_df.merge(
    market_df,
    on=["company_id", "year"],
    how="left",
)

print("\nAfter Market Cap Merge")
print(financial_df.shape)

financial_df = financial_df.merge(
    analysis_df,
    on="company_id",
    how="left",
)

print("\nAfter Analysis Merge")
print(financial_df.shape)

profit_df = profit_df.drop_duplicates(
    subset=["company_id", "year"]
)

financial_df = financial_df.merge(
    profit_df,
    on=["company_id", "year"],
    how="left",
)

print("\nAfter Profit Merge")
print(financial_df.shape)



# ==========================================
# Load YAML Config
# ==========================================

with open(CONFIG_PATH, "r") as file:
    config = yaml.safe_load(file)

# ==========================================
# Display Information
# ==========================================

print("=" * 60)
print("FINANCIAL RATIOS")
print("=" * 60)
print("Rows :", len(financial_df))
print("Columns:")
print(financial_df.columns.tolist())

print("\n" + "=" * 60)
print("COMPANIES")
print("=" * 60)
print("Rows :", len(companies_df))
print("Columns:")
print(companies_df.columns.tolist())

print("\n" + "=" * 60)
print("SCREENER CONFIG")
print("=" * 60)
print(config)

# ==========================================
# Generic Screener Function
# ==========================================

def apply_filters(df, settings):

    result = df.copy()

    # ROE
    if (
        "roe_min" in settings
        and "return_on_equity_pct" in result.columns
    ):
        result = result[
            result["return_on_equity_pct"] >= settings["roe_min"]
        ]

    # Debt to Equity
    if (
        "debt_to_equity_max" in settings
        and "debt_to_equity" in result.columns
    ):
        result = result[
            result["debt_to_equity"] <= settings["debt_to_equity_max"]
        ]

    # Free Cash Flow
    if (
        "free_cash_flow_min" in settings
        and "free_cash_flow_cr" in result.columns
    ):
        result = result[
            result["free_cash_flow_cr"] >= settings["free_cash_flow_min"]
        ]

    # Operating Profit Margin
    if (
        "operating_profit_margin_min" in settings
        and "operating_profit_margin_pct" in result.columns
    ):
        result = result[
            result["operating_profit_margin_pct"]
            >= settings["operating_profit_margin_min"]
        ]

    # Interest Coverage
    if (
        "interest_coverage_min" in settings
        and "interest_coverage" in result.columns
    ):
        result = result[
            result["interest_coverage"]
            >= settings["interest_coverage_min"]
        ]

    # Asset Turnover
    if (
        "asset_turnover_min" in settings
        and "asset_turnover" in result.columns
    ):
        result = result[
            result["asset_turnover"]
            >= settings["asset_turnover_min"]
        ]

    # Revenue CAGR
    if (
        "revenue_cagr_5yr_min" in settings
        and "revenue_cagr_5yr" in result.columns
    ):
        result = result[
            result["revenue_cagr_5yr"]
            >= settings["revenue_cagr_5yr_min"]
        ]

    return result


# ==========================================
# Composite Quality Score
# ==========================================

def add_composite_score(df):

    result = df.copy()

    # Fill missing values
    score_columns = [
        "return_on_equity_pct",
        "net_profit_margin_pct",
        "free_cash_flow_cr",
        "asset_turnover",
        "debt_to_equity",
    ]

    for col in score_columns:
       result[col] = result[col].fillna(0)

    # Normalize each metric (0-100)
    result["roe_score"] = (
        result["return_on_equity_pct"]
        / result["return_on_equity_pct"].max()
    ) * 100

    result["npm_score"] = (
        result["net_profit_margin_pct"]
        / result["net_profit_margin_pct"].max()
    ) * 100

    result["fcf_score"] = (
        result["free_cash_flow_cr"]
        / result["free_cash_flow_cr"].max()
    ) * 100

    result["asset_score"] = (
        result["asset_turnover"]
        / result["asset_turnover"].max()
    ) * 100

    # Lower Debt-to-Equity is better
   # Lower Debt-to-Equity is better
    max_de = result["debt_to_equity"].max()

    if max_de == 0:
        result["de_score"] = 100
    else:
        result["de_score"] = (
            1 - (result["debt_to_equity"] / max_de)
        ) * 100

    # Weighted Composite Score
    result["composite_quality_score"] = (
        result["roe_score"] * 0.35
        + result["npm_score"] * 0.20
        + result["fcf_score"] * 0.20
        + result["asset_score"] * 0.10
        + result["de_score"] * 0.15
    )

    return result


# ==========================================
# Run Screener
# ==========================================

def run_screener(title, config_key, output_file):

    settings = config[config_key]

    df = apply_filters(
        financial_df,
        settings,
    )

    # Add Composite Score
    df = add_composite_score(df)

    # Sort by Composite Score
    df = df.sort_values(
        by="composite_quality_score",
        ascending=False,
    )

    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)
    print("Companies Found :", len(df))

    DISPLAY_COLUMNS = [
        "company_id",
        "company_name",
        "year",
        "return_on_equity_pct",
        "debt_to_equity",
        "free_cash_flow_cr",
        "composite_quality_score",
    ]

    print(df[DISPLAY_COLUMNS].head(20))

    df.to_excel(
        OUTPUT_DIR / output_file,
        index=False,
    )

    print("\nSaved:")
    print(OUTPUT_DIR / output_file)

    return df


# ==========================================
# Execute All Screeners
# ==========================================

SCREENERS = [
    (
        "QUALITY COMPOUNDER",
        "quality_compounder",
        "quality_compounder.xlsx",
    ),
    (
        "VALUE PICK",
        "value_pick",
        "value_pick.xlsx",
    ),
    (
        "GROWTH ACCELERATOR",
        "growth_accelerator",
        "growth_accelerator.xlsx",
    ),
    (
        "DIVIDEND CHAMPION",
        "dividend_champion",
        "dividend_champion.xlsx",
    ),
    (
        "DEBT FREE BLUE CHIP",
        "debt_free_blue_chip",
        "debt_free_blue_chip.xlsx",
    ),
    (
        "TURNAROUND WATCH",
        "turnaround_watch",
        "turnaround_watch.xlsx",
    ),
]

# Store all screener results
results = {}

# Execute each screener
for title, config_key, output_file in SCREENERS:
    results[config_key] = run_screener(
        title,
        config_key,
        output_file,
    )

# ==========================================
# Create Combined Excel Workbook
# ==========================================

combined_file = OUTPUT_DIR / "screener_output.xlsx"

with pd.ExcelWriter(combined_file, engine="openpyxl") as writer:

    for title, config_key, output_file in SCREENERS:

        sheet_name = title[:31]

        results[config_key].to_excel(
            writer,
            sheet_name=sheet_name,
            index=False,
        )

print("\nCombined Screener Workbook Saved:")
print(combined_file)

# Close database connection
conn.close()

print("\n" + "=" * 60)
print("ALL SCREENERS COMPLETED SUCCESSFULLY")
print("=" * 60)
print(f"Output folder: {OUTPUT_DIR}")