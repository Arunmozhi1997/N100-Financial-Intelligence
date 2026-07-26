import sqlite3
import pandas as pd

DB_PATH = "db/nifty100.db"


def load_data():
    """Load required tables from SQLite."""

    conn = sqlite3.connect(DB_PATH)

    financial = pd.read_sql(
        "SELECT * FROM financial_ratios",
        conn,
    )

    peer = pd.read_sql(
        "SELECT * FROM peer_percentiles",
        conn,
    )

    companies = pd.read_sql(
        "SELECT * FROM companies",
        conn,
    )

    conn.close()

    return financial, peer, companies


def performance_label(percentile):
    """Return performance label."""

    if percentile >= 90:
        return "Excellent"

    elif percentile >= 75:
        return "Strong"

    elif percentile >= 50:
        return "Average"

    else:
        return "Needs Improvement"


def company_report(company_id, financial, peer):
    """Display a company analytics report."""

    latest = (
        financial[
            financial["company_id"] == company_id
        ]
        .sort_values("year")
        .tail(1)
    )

    if latest.empty:
        print("\nCompany not found.")
        return

    latest = latest.iloc[0]

    print("\n" + "=" * 70)
    print(f"COMPANY REPORT : {company_id}")
    print("=" * 70)

    print(f"\nFinancial Year : {latest['year']}")

    metrics = [
        "return_on_equity_pct",
        "net_profit_margin_pct",
        "debt_to_equity",
        "free_cash_flow_cr",
        "interest_coverage",
        "asset_turnover",
    ]

    print("\nFINANCIAL METRICS")
    print("-" * 70)

    for metric in metrics:

        value = latest[metric]

        print(
            f"{metric:<30} : {value:>12.2f}"
        )

    print("\nPEER PERCENTILES")
    print("-" * 70)

    company_peer = (
        peer[
            peer["company_id"] == company_id
        ]
        .sort_values("year")
    )

    if company_peer.empty:
        print("No peer percentile data available.")
        return

    for metric in metrics:

        row = company_peer[
            company_peer["metric"] == metric
        ]

        if row.empty:
            continue

        percentile = row.iloc[-1]["percentile_rank"]

        label = performance_label(percentile)

        print(
            f"{metric:<30} : "
            f"{percentile:>6.1f}%   {label}"
        )


if __name__ == "__main__":

    financial, peer, companies = load_data()

    company_report(
        "TCS",
        financial,
        peer,
    )