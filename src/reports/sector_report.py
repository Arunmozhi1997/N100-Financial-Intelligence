import os
import sqlite3

import pandas as pd

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

DB_PATH = "db/nifty100.db"

OUTPUT_FOLDER = "reports/sector"

os.makedirs(
    OUTPUT_FOLDER,
    exist_ok=True,
)

def load_sector_data():

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        """
        SELECT
            c.company_name,
            s.broad_sector,
            r.return_on_equity_pct,
            c.roce_percentage,
            r.operating_profit_margin_pct,
            r.net_profit_margin_pct,
            r.debt_to_equity
        FROM companies c

        JOIN sectors s
        ON c.id = s.company_id

        JOIN financial_ratios r
        ON c.id = r.company_id
        """,
        conn,
    )

    conn.close()

    # Latest year only
    df = (
        df.sort_values("company_name")
        .groupby("company_name")
        .tail(1)
    )

    return df

def create_sector_report(sector_name, data):

    pdf_path = os.path.join(
        OUTPUT_FOLDER,
        f"{sector_name}.pdf",
    )

    doc = SimpleDocTemplate(pdf_path)

    styles = getSampleStyleSheet()

    story = []

    # ----------------------------
    # Title
    # ----------------------------

    story.append(
        Paragraph(
            f"<b>{sector_name}</b>",
            styles["Title"],
        )
    )

    story.append(Spacer(1, 20))

    # ----------------------------
    # Sector Summary
    # ----------------------------

    summary = [
        ["Companies", len(data)],
        ["Median ROE", f"{data['return_on_equity_pct'].median():.2f}%"],
        ["Median ROCE", f"{data['roce_percentage'].median():.2f}%"],
        ["Median OPM", f"{data['operating_profit_margin_pct'].median():.2f}%"],
        ["Median NPM", f"{data['net_profit_margin_pct'].median():.2f}%"],
        ["Median D/E", f"{data['debt_to_equity'].median():.2f}"],
    ]

    summary_table = Table(
        summary,
        colWidths=[180, 180],
    )

    summary_table.setStyle(
        TableStyle(
            [
                ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
                ("BACKGROUND", (0,0), (0,-1), colors.lightgrey),
                ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0,0), (-1,-1), 6),
            ]
        )
    )

    story.append(summary_table)

    story.append(Spacer(1, 20))

# ----------------------------
# Company Comparison
# ----------------------------

    story.append(
        Paragraph(
           "<b>Company Comparison</b>",
            styles["Heading2"],
        )
    )

    story.append(Spacer(1, 10))

    table_data = [
       [
        "Company",
        "ROE",
        "ROCE",
        "OPM",
        "NPM",
        "D/E",
       ]
    ]

    for _, row in data.iterrows():

        table_data.append(
           [
            row["company_name"],
            f"{row['return_on_equity_pct']:.2f}%",
            f"{row['roce_percentage']:.2f}%",
            f"{row['operating_profit_margin_pct']:.2f}%",
            f"{row['net_profit_margin_pct']:.2f}%",
            f"{row['debt_to_equity']:.2f}",
           ]
        )

    comparison_table = Table(
        table_data,
        colWidths=[180, 60, 60, 60, 60, 50],
    )

    comparison_table.setStyle(
        TableStyle(
           [
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ALIGN", (1, 1), (-1, -1), "CENTER"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
           ]
        )
    )
 
    story.append(comparison_table)
 
    doc.build(story)

    print(f"✓ {sector_name}")

def main():

    df = load_sector_data()

    sectors = sorted(df["broad_sector"].unique())

    print(f"\nGenerating {len(sectors)} sector reports...\n")

    for sector in sectors:

        sector_df = df[
            df["broad_sector"] == sector
        ]

        create_sector_report(
            sector,
            sector_df,
        )

    print("\nAll sector reports generated successfully.")


if __name__ == "__main__":
    main()