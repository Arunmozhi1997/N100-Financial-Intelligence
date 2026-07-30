import sqlite3
from pathlib import Path

import pandas as pd

# --------------------------------------------------
# Paths
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "db" / "nifty100.db"
OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

# --------------------------------------------------
# Load Data
# --------------------------------------------------
conn = sqlite3.connect(DB_PATH)

query = """
SELECT
    c.id AS company_id,
    c.company_name,
    s.broad_sector,
    m.year,
    m.pe_ratio,
    m.pb_ratio,
    m.ev_ebitda,
    m.market_cap_crore,
    r.free_cash_flow_cr
FROM companies c

LEFT JOIN sectors s
    ON c.id = s.company_id

LEFT JOIN market_cap m
    ON c.id = m.company_id

LEFT JOIN financial_ratios r
    ON m.company_id = r.company_id
   AND CAST(m.year AS INTEGER) = CAST(r.year AS INTEGER)

ORDER BY
    c.id,
    m.year DESC
"""

df = pd.read_sql(query, conn)

conn.close()

# --------------------------------------------------
# Convert Year
# --------------------------------------------------
df["year"] = pd.to_numeric(df["year"], errors="coerce")

latest_year = int(df["year"].max())

# --------------------------------------------------
# Company 5-Year Median PE
# --------------------------------------------------
five_year = df[df["year"] >= latest_year - 4].copy()

company_pe = five_year.groupby("company_id")["pe_ratio"].median().reset_index()

company_pe.columns = [
    "company_id",
    "5yr_median_PE",
]

# --------------------------------------------------
# Latest Year
# --------------------------------------------------
latest = df[df["year"] == latest_year].copy()

latest = latest.merge(
    company_pe,
    on="company_id",
    how="left",
)

print(f"Latest Year : {latest_year}")
print(f"Companies   : {len(latest)}")

# --------------------------------------------------
# FCF Yield
# --------------------------------------------------
latest["FCF_yield_pct"] = (
    latest["free_cash_flow_cr"] / latest["market_cap_crore"] * 100
).round(2)

# --------------------------------------------------
# Sector Median PE (Latest Year)
# --------------------------------------------------
sector_pe = latest.groupby("broad_sector")["pe_ratio"].median().reset_index()

sector_pe.columns = [
    "broad_sector",
    "sector_median_pe",
]

latest = latest.merge(
    sector_pe,
    on="broad_sector",
    how="left",
)

# --------------------------------------------------
# PE vs Sector Median
# --------------------------------------------------
latest["PE_vs_sector_median_pct"] = (
    (latest["pe_ratio"] - latest["sector_median_pe"]) / latest["sector_median_pe"] * 100
).round(2)


# --------------------------------------------------
# Valuation Flag
# --------------------------------------------------
def get_flag(row):

    if pd.isna(row["pe_ratio"]) or pd.isna(row["sector_median_pe"]):
        return "N/A"

    if row["pe_ratio"] > row["sector_median_pe"] * 1.5:
        return "Caution"

    if row["pe_ratio"] < row["sector_median_pe"] * 0.7:
        return "Discount"

    return "Fair"


latest["flag"] = latest.apply(
    get_flag,
    axis=1,
)

# --------------------------------------------------
# Final Output
# --------------------------------------------------
valuation_summary = latest[
    [
        "company_id",
        "company_name",
        "broad_sector",
        "pe_ratio",
        "pb_ratio",
        "ev_ebitda",
        "FCF_yield_pct",
        "5yr_median_PE",
        "sector_median_pe",
        "PE_vs_sector_median_pct",
        "flag",
    ]
].copy()

valuation_summary.rename(
    columns={
        "broad_sector": "sector",
    },
    inplace=True,
)

valuation_summary.to_excel(
    OUTPUT_DIR / "valuation_summary.xlsx",
    index=False,
)

valuation_flags = valuation_summary[
    valuation_summary["flag"].isin(["Caution", "Discount"])
]

valuation_flags.to_csv(
    OUTPUT_DIR / "valuation_flags.csv",
    index=False,
)

print("\nDone!")
print("valuation_summary.xlsx created")
print("valuation_flags.csv created")

print("\nFlag Counts")
print(valuation_summary["flag"].value_counts())
