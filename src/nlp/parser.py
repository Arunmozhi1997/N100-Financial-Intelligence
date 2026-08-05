import re
from pathlib import Path

import pandas as pd

# Project paths
BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "data" / "raw"
OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

ANALYSIS_FILE = RAW_DIR / "analysis.xlsx"

PATTERN = re.compile(
    r"(TTM|Last Year|\d+\s*Years?|\d+\s*Year)\s*:?\s*(-?[\d.]+)%"
)

def extract_metric(text):
    if pd.isna(text):
        return None

    text = str(text).strip()

    match = PATTERN.search(text)

    if not match:
        return None

    period = match.group(1)
    value = float(match.group(2))

    if period == "TTM":
        years = 0
    elif period == "Last Year":
        years = 1
    else:
        years = int(re.search(r"\d+", period).group())

    return years, value

def main():

    df = pd.read_excel(ANALYSIS_FILE, skiprows=1)

    parsed_rows = []
    failed_rows = []

    metrics = [
        "compounded_sales_growth",
        "compounded_profit_growth",
        "stock_price_cagr",
        "roe",
    ]

    for _, row in df.iterrows():

        for metric in metrics:

            result = extract_metric(row[metric])

            if result:

                years, value = result

                parsed_rows.append({
                    "company_id": row["company_id"],
                    "metric_type": metric,
                    "period_years": years,
                    "value_pct": value,
                })

            else:

                failed_rows.append({
                    "company_id": row["company_id"],
                    "metric_type": metric,
                    "original_text": row[metric],
                })

    parsed_df = pd.DataFrame(parsed_rows)
    failed_df = pd.DataFrame(failed_rows)

    parsed_df.to_csv(
        OUTPUT_DIR / "analysis_parsed.csv",
        index=False
    )

    failed_df.to_csv(
        OUTPUT_DIR / "parse_failures.csv",
        index=False
    )

    print(f"Parsed rows : {len(parsed_df)}")
    print(f"Failed rows : {len(failed_df)}")



if __name__ == "__main__":
    main()