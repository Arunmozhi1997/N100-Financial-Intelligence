import os
import sqlite3
import pandas as pd

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)

DB_PATH = "db/nifty100.db"

OUTPUT_FOLDER = "reports/portfolio"

os.makedirs(
    OUTPUT_FOLDER,
    exist_ok=True,
)

def load_data():

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        """
        SELECT
            c.company_name,
            c.roce_percentage,
            s.broad_sector,
            r.return_on_equity_pct,
            r.net_profit_margin_pct,
            r.operating_profit_margin_pct,
            r.debt_to_equity,
            r.earnings_per_share

        FROM companies c

        JOIN sectors s
        ON c.id=s.company_id

        JOIN financial_ratios r
        ON c.id=r.company_id
        """,
        conn,
    )

    conn.close()

    df = (
        df.sort_values("company_name")
        .groupby("company_name")
        .tail(1)
    )

    return df

def arrow(value):

    if value >= 20:
        return "↑"

    elif value >= 10:
        return "→"

    else:
        return "↓"

def build_pdf(df):

    pdf = os.path.join(
        OUTPUT_FOLDER,
        "portfolio_summary.pdf",
    )

    doc = SimpleDocTemplate(pdf)

    styles = getSampleStyleSheet()

    story = []

    for _, row in df.iterrows():

        story.append(
            Paragraph(
                f"<b>{row['company_name']}</b>",
                styles["Title"],
            )
        )

        story.append(
            Paragraph(
                f"Sector : {row['broad_sector']}",
                styles["Heading2"],
            )
        )

        story.append(Spacer(1,15))

        table = [
            ["Metric","Value","Trend"],

            [
                "ROE",
                f"{row['return_on_equity_pct']:.2f}%",
                arrow(row["return_on_equity_pct"]),
            ],

            [
                "ROCE",
                f"{row['roce_percentage']:.2f}%",
                arrow(row["roce_percentage"]),
            ],

            [
                "OPM",
                f"{row['operating_profit_margin_pct']:.2f}%",
                arrow(row["operating_profit_margin_pct"]),
            ],

            [
                "NPM",
                f"{row['net_profit_margin_pct']:.2f}%",
                arrow(row["net_profit_margin_pct"]),
            ],

            [
                "D/E",
                f"{row['debt_to_equity']:.2f}",
                "↓" if row["debt_to_equity"]<1 else "↑",
            ],

            [
                "EPS",
                f"{row['earnings_per_share']:.2f}",
                arrow(row["earnings_per_share"]/20),
            ],
        ]

        t = Table(
            table,
            colWidths=[120,120,60],
        )

        t.setStyle(
            TableStyle(
                [
                    ("GRID",(0,0),(-1,-1),0.5,colors.grey),
                    ("BACKGROUND",(0,0),(-1,0),colors.darkblue),
                    ("TEXTCOLOR",(0,0),(-1,0),colors.white),
                    ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
                    ("ALIGN",(1,1),(-1,-1),"CENTER"),
                ]
            )
        )

        story.append(t)

        story.append(PageBreak())

    doc.build(story)

    print("Saved:",pdf)


def main():

    df = load_data()

    build_pdf(df)


if __name__ == "__main__":
    main()