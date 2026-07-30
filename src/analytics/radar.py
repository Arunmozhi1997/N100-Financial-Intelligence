import os
import sqlite3

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

DB_PATH = "db/nifty100.db"
PEER_FILE = "data/raw/peer_groups.xlsx"

OUTPUT_DIR = "reports/radar_charts"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_data():
    """Load data from database."""

    conn = sqlite3.connect(DB_PATH)

    financial = pd.read_sql(
        "SELECT * FROM financial_ratios",
        conn,
    )

    analysis = pd.read_sql(
        "SELECT * FROM analysis",
        conn,
    )

    conn.close()

    peer = pd.read_excel(PEER_FILE)

    return financial, analysis, peer


def prepare_data(financial, analysis, peer):
    """Merge all required datasets."""

    df = financial.merge(
        analysis,
        on="company_id",
        how="left",
    )

    df = df.merge(
        peer,
        on="company_id",
        how="left",
    )

    print("\nMerged Data")
    print(df.shape)

    return df


def create_radar(company):
    """Generate one radar chart."""

    labels = [
        "ROE",
        "NPM",
        "Debt/Equity",
        "FCF",
        "ICR",
        "Asset Turnover",
    ]

    values = [
        company["return_on_equity_pct"],
        company["net_profit_margin_pct"],
        company["debt_to_equity"],
        company["free_cash_flow_cr"],
        company["interest_coverage"],
        company["asset_turnover"],
    ]

    # Replace missing values
    values = [0 if pd.isna(x) else float(x) for x in values]

    # Normalize values to 0-100
    normalized = []

    for value in values:
        if value < 0:
            value = 0
        if value > 100:
            value = 100
        normalized.append(value)

    normalized += normalized[:1]

    angles = np.linspace(
        0,
        2 * np.pi,
        len(labels),
        endpoint=False,
    ).tolist()

    angles += angles[:1]

    plt.figure(figsize=(6, 6))

    ax = plt.subplot(111, polar=True)

    ax.plot(
        angles,
        normalized,
        linewidth=2,
    )

    ax.fill(
        angles,
        normalized,
        alpha=0.25,
    )

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)

    ax.set_ylim(0, 100)

    plt.title(company["company_id"])

    filename = os.path.join(
        OUTPUT_DIR,
        f"{company['company_id']}_radar.png",
    )

    plt.savefig(
        filename,
        dpi=200,
        bbox_inches="tight",
    )

    plt.close()


def generate_all_radars(df):
    """Generate radar chart for every company."""

    latest = df.sort_values("year").groupby("company_id").tail(1)

    print("\nGenerating Radar Charts...")

    count = 0

    for _, row in latest.iterrows():
        create_radar(row)
        count += 1

    print(f"\nGenerated {count} radar charts.")
    print(f"Saved to: {OUTPUT_DIR}")


if __name__ == "__main__":

    financial, analysis, peer = load_data()

    print("\nFinancial Ratios")
    print(financial.shape)

    print("\nAnalysis")
    print(analysis.shape)

    print("\nPeer Groups")
    print(peer.shape)

    merged = prepare_data(
        financial,
        analysis,
        peer,
    )

    generate_all_radars(merged)
