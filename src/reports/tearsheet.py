import sqlite3
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    PageBreak,
)

DB_PATH = "db/nifty100.db"

OUTPUT_FOLDER = "reports/tearsheets"

os.makedirs(
    OUTPUT_FOLDER,
    exist_ok=True,
)

CHART_FOLDER = "reports/charts"
PROS_CONS_FILE = "output/pros_cons_generated.csv"

os.makedirs(
    CHART_FOLDER,
    exist_ok=True,
)


def load_company(company_id):

    conn = sqlite3.connect(DB_PATH)

    company = pd.read_sql(
        f"""
        SELECT *
        FROM companies
        WHERE id='{company_id}'
        """,
        conn,
    )

    ratios = pd.read_sql(
        f"""
        SELECT *
        FROM financial_ratios
        WHERE company_id='{company_id}'
        ORDER BY year
        """,
        conn,
    )

    profit_loss = pd.read_sql(
        f"""
        SELECT year, sales, net_profit
        FROM profitandloss
        WHERE company_id='{company_id}'
        ORDER BY year
       """,
        conn,
    )

    sector = pd.read_sql(
        f"""
        SELECT
           broad_sector,
           sub_sector,
           market_cap_category
        FROM sectors
        WHERE company_id='{company_id}'
        """,
        conn,
    )

    cashflow = pd.read_sql(
        f"""
        SELECT
           year,
           operating_activity,
           investing_activity,
           financing_activity
        FROM cashflow
        WHERE company_id='{company_id}'
        ORDER BY year
        """,
        conn,
    )

    capital = pd.read_sql(
        f"""
        SELECT
            year,
            capital_allocation_label,
            cashflow_score,
            cashflow_grade
        FROM cashflow_intelligence
        WHERE company_id='{company_id}'
        ORDER BY year
        """,
        conn,
    )

    stock_price = pd.read_sql(
        f"""
        SELECT
           date,
           close_price
        FROM stock_prices
        WHERE company_id='{company_id}'
        ORDER BY date
        """,
        conn,
    )

    valuation = pd.read_sql(
        f"""
        SELECT
            year,
            market_cap_crore,
            pe_ratio,
            pb_ratio,
            dividend_yield_pct
        FROM market_cap
        WHERE company_id='{company_id}'
        ORDER BY year
        """,
        conn,
    )

    conn.close()

    return (
    company,
    ratios,
    profit_loss,
    cashflow,
    sector,
    capital,
    stock_price, 
    valuation,
    
    )

def load_peers(company_id):

    conn = sqlite3.connect(DB_PATH)

    # Find company's sub-sector
    sector = pd.read_sql(
        f"""
        SELECT sub_sector
        FROM sectors
        WHERE company_id='{company_id}'
        """,
        conn,
    )

    if sector.empty:
        conn.close()
        return pd.DataFrame()

    sub_sector = sector.iloc[0]["sub_sector"]

    peers = pd.read_sql(
        f"""
        SELECT

            c.company_name,

            s.company_id,

            c.roce_percentage,

            c.roe_percentage,

            r.net_profit_margin_pct,

            r.debt_to_equity

        FROM sectors s

        JOIN companies c
            ON s.company_id = c.id

        JOIN financial_ratios r
            ON s.company_id = r.company_id

        WHERE

            s.sub_sector='{sub_sector}'

        AND

            r.year=(
                SELECT MAX(year)
                FROM financial_ratios fr
                WHERE fr.company_id=r.company_id
            )

        ORDER BY

            c.roce_percentage DESC
        """,
        conn,
    )

    conn.close()

    return peers

def load_pros_cons(company_id):

    if not os.path.exists(PROS_CONS_FILE):
        return [], []

    df = pd.read_csv(PROS_CONS_FILE)

    df = df[df["company_id"] == company_id]

    pros = (
        df[df["type"] == "pro"]["text"]
        .head(5)
        .tolist()
    )

    cons = (
        df[df["type"] == "con"]["text"]
        .head(5)
        .tolist()
    )

    return pros, cons



def create_tearsheet(company_id):

    company, ratios, profit_loss, cashflow, sector, capital, stock_price, valuation = load_company(company_id)
    peers = load_peers(company_id)
    pros, cons = load_pros_cons(company_id)

    if company.empty:
        print("Company not found")
        return

    pdf_file = os.path.join(
        OUTPUT_FOLDER,
        f"{company_id}_tearsheet.pdf",
    )

    doc = SimpleDocTemplate(
        pdf_file,
        pagesize=A4,
    )

    styles = getSampleStyleSheet()

    story = []

    # ----------------------------
    # Header
    # ----------------------------

    company_name = company.iloc[0]["company_name"]
    roce = company.iloc[0]["roce_percentage"]

    header = Table(
        [[
            Paragraph(
                f"<font color='white'><b>{company_name}</b></font>",
                styles["Heading1"],
            )
        ]],
        colWidths=[500],
    )

    header.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.darkblue),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("TOPPADDING", (0, 0), (-1, -1), 12),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
            ]
        )
    )

    story.append(header)
    story.append(Spacer(1, 20))


# ---------------------------------
# Company Overview
# ---------------------------------

    overview = [
    [
        "Company",
        company.iloc[0]["company_name"],
    ],

    [
        "Sector",
        sector.iloc[0]["broad_sector"] if not sector.empty else "N/A",
    ],

    [
        "Industry",
        sector.iloc[0]["sub_sector"] if not sector.empty else "N/A",
    ],

    [
        "Market Cap",
        sector.iloc[0]["market_cap_category"] if not sector.empty else "N/A",
    ],

    [
        "ROCE",
        f"{company.iloc[0]['roce_percentage']:.2f}%",
    ],

    [
        "ROE",
        f"{company.iloc[0]['roe_percentage']:.2f}%",
    ],
]

    overview_table = Table(
        overview,
        colWidths=[150, 300],
    )

    overview_table.setStyle(
        TableStyle(
        [
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),

            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#E8EEF7")),

            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),

            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),

            ("TOPPADDING", (0, 0), (-1, -1), 8),
        ]
    )
)

    
    

   
# ----------------------------
# Revenue Chart
# ----------------------------

    profit_loss = profit_loss.sort_values("year")

    plt.figure(figsize=(8,3))

    plt.bar(
       profit_loss["year"].astype(str),
       profit_loss["sales"],
    )

    plt.title("Revenue Trend")
    plt.xlabel("Year")
    plt.ylabel("Sales")

    chart_path = os.path.join(
        CHART_FOLDER,
        f"{company_id}_revenue.png",
    )

    plt.tight_layout()

    plt.savefig(chart_path)

    plt.close() 

# ----------------------------
# Profit Chart
# ----------------------------

    plt.figure(figsize=(8,3))

    plt.bar(
       profit_loss["year"].astype(str),
       profit_loss["net_profit"],
    )

    plt.title("Net Profit Trend")
    plt.xlabel("Year")
    plt.ylabel("Net Profit")

    profit_chart_path = os.path.join(
       CHART_FOLDER,
       f"{company_id}_profit.png",
    )

    plt.tight_layout()

    plt.savefig(profit_chart_path)

    plt.close()

# ----------------------------
# ROE vs ROCE Chart
# ----------------------------

    plt.figure(figsize=(8,3))

    plt.plot(
       ratios["year"],
       ratios["return_on_equity_pct"],
       marker="o",
       linewidth=2,
       label="ROE",
    )

    plt.plot(
       ratios["year"],
       [roce] * len(ratios),
       linestyle="--",
       linewidth=2,
       label="ROCE",
    )

    plt.title("ROE vs ROCE")
    plt.xlabel("Year")
    plt.ylabel("Percentage")
 
    plt.xticks(
       ratios["year"],
       rotation=45,
    )

    plt.legend()

    plt.tight_layout()

    roe_chart_path = os.path.join(
       CHART_FOLDER,
       f"{company_id}_roe_roce.png",
    )

    plt.savefig(roe_chart_path)

    plt.close()


# ----------------------------
# Radar Chart
# ----------------------------


    latest = ratios.sort_values("year").iloc[-1]

    overall_score = round(
       (
           latest["return_on_equity_pct"]
           + company.iloc[0]["roce_percentage"]
           + latest["net_profit_margin_pct"]
           + capital.iloc[-1]["cashflow_score"]
        ) / 4
    )


#rating


    if overall_score >= 90:
        rating = "★★★★★"

    elif overall_score >= 75:
        rating = "★★★★☆"

    elif overall_score >= 60:
        rating = "★★★☆☆"

    elif overall_score >= 45:
        rating = "★★☆☆☆"

    else:
        rating = "★☆☆☆☆"

#recommendation

    if overall_score >= 80:
       recommendation = "BUY"

    elif overall_score >= 60:
       recommendation = "HOLD"

    else:
       recommendation = "AVOID"

#financial health

    if latest["debt_to_equity"] < 0.5:
        health = "Excellent"

    elif latest["debt_to_equity"] < 1:
        health = "Good"

    else:
        health = "Weak"

    summary_data = [
        ["Overall Rating", rating],
        ["Quality Score", f"{overall_score}/100"],
        ["Financial Health", health],
        ["Capital Allocation", capital.iloc[-1]["capital_allocation_label"]],
        ["Recommendation", recommendation],
    ]


    summary_table = Table(
        summary_data,
        colWidths=[180, 220],
    )

    summary_table.setStyle(
        TableStyle(
           [
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#EAF2F8")),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
           ]
        )
    )


    story.append(
        Paragraph(
           "<b>Investment Summary</b>",
           styles["Heading2"],
        )
    )

    story.append(Spacer(1,8))

    story.append(summary_table)

    story.append(Spacer(1,20))

    profitability = min(
        latest["return_on_equity_pct"], 50
    ) / 50 * 100

    efficiency = min(
        roce, 50
    ) / 50 * 100

    margin = min(
        latest["net_profit_margin_pct"], 30
    ) / 30 * 100

    leverage = max(
        0,
        100 - latest["debt_to_equity"] * 50,
    )

    cashflow_score = (
        capital.iloc[-1]["cashflow_score"]
        if not capital.empty
        else 50
    )

    categories = [
        "Profitability",
        "Efficiency",
        "Margin",
        "Leverage",
        "Cash Flow",
    ]

    values = [
        profitability,
        efficiency,
        margin,
        leverage,
        cashflow_score,
    ]

    radar_score = int(sum(values) / len(values))

    values += values[:1]

    angles = np.linspace(
        0,
        2 * np.pi,
        len(categories),
          endpoint=False,
        ).tolist()

    angles += angles[:1]

    plt.figure(figsize=(6, 6))

    ax = plt.subplot(
       111,
       polar=True,
    )

# Blue outline
    ax.plot(
       angles,
       values,
       color="#1565C0",
       linewidth=3.5,
    )

# Blue fill
    ax.fill(
       angles,
       values,
       color="#42A5F5",
       alpha=0.20,
    )

# Category labels
    ax.set_xticks(angles[:-1])

    ax.set_xticklabels(
      categories,
      fontsize=12,
      fontweight="bold",
    )

# Scale
    ax.set_ylim(0, 100)

    ax.set_yticks(
       [20, 40, 60, 80, 100]
    )

    ax.set_yticklabels([])

# Grid
    ax.grid(
       color="#DDDDDD",
       linestyle="--",
       linewidth=0.8,
    )

# radar score
    ax.text(
       0,
       0,
       f"{radar_score}",
       fontsize=24,
       fontweight="bold",
       color="#0D47A1",
       ha="center",
       va="center",
    )

    ax.text(
       0,
       -12,
       "QUALITY SCORE",
       fontsize=9,
       color="grey",
       ha="center",      

    )

    

    radar_chart = os.path.join(
       CHART_FOLDER,
       f"{company_id}_radar.png",
    )

    plt.tight_layout()

    plt.savefig(
       radar_chart,
       dpi=300,
    ) 

    plt.close()



    revenue_image = Image(
       chart_path,
       width=240,
       height=180,
    )

    profit_image = Image(
       profit_chart_path,
       width=240,
       height=180,
    )

    charts_table = Table(
    [
        [revenue_image, profit_image]
    ],
    colWidths=[250, 250],
)

    charts_table.setStyle(
    TableStyle(
        [
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]
    )
)

    story.append(
      Paragraph(
        "<b>10 Year Financial Trends</b>",
        styles["Heading2"],
     )
    )

    story.append(Spacer(1,10))

    story.append(charts_table)

    story.append(Spacer(1,20))

    story.append(
    Image(
        roe_chart_path,
        width=450,
        height=220,
    )
)

    story.append(Spacer(1,20))

    latest_pattern = capital.iloc[-1]["capital_allocation_label"]

    story.append(
        Paragraph(
           "<b>Capital Allocation Pattern</b>",
            styles["Heading2"],
        )
    )

    badge = Table(
        [[latest_pattern]],
        colWidths=[250],
    )

    badge.setStyle(
        TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, -1), colors.darkgreen),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 14),
            ("TOPPADDING", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ]
    )
)

    story.append(badge)
    story.append(Spacer(1, 20))

    # ----------------------------
    # KPI Tiles
    # ----------------------------

    latest = ratios.sort_values("year").iloc[-1]

    kpi_data = [
    [
        Paragraph("<b>ROE</b>", styles["BodyText"]),
        Paragraph(f"{latest['return_on_equity_pct']:.2f}%", styles["BodyText"]),
    ],
    [
        Paragraph("<b>ROCE</b>", styles["BodyText"]),
        Paragraph(f"{roce:.2f}%", styles["BodyText"]),
    ],
    [
        Paragraph("<b>NPM</b>", styles["BodyText"]),
        Paragraph(f"{latest['net_profit_margin_pct']:.2f}%", styles["BodyText"]),
    ],
    [
        Paragraph("<b>OPM</b>", styles["BodyText"]),
        Paragraph(f"{latest['operating_profit_margin_pct']:.2f}%", styles["BodyText"]),
    ],
    [
        Paragraph("<b>D/E</b>", styles["BodyText"]),
        Paragraph(f"{latest['debt_to_equity']:.2f}", styles["BodyText"]),
    ],
    [
        Paragraph("<b>EPS</b>", styles["BodyText"]),
        Paragraph(f"{latest['earnings_per_share']:.2f}", styles["BodyText"]),
    ],
]

    kpi_table = Table(
        kpi_data,
        colWidths=[180, 120],
    )

    kpi_table.setStyle(
        TableStyle(
        [
            ("GRID", (0, 0), (-1, -1), 1, colors.grey),
            ("BACKGROUND", (0, 0), (-1, -1), colors.beige),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
        ]
    )
)

    story.append(kpi_table)
    story.append(Spacer(1, 25))



# ----------------------------
# Pros
# ----------------------------

    story.append(
        Paragraph(
           "<b>Pros</b>",
            styles["Heading2"],
        )
    )

    if len(pros) == 0:
        story.append(
            Paragraph(
               "No pros available.",
                styles["BodyText"],
            )
        )
    else:
        for p in pros:
            story.append(
                Paragraph(
                    f"• {p}",
                    styles["BodyText"],
                )
            )

    story.append(Spacer(1,12))


# ----------------------------
# Cons
# ----------------------------

    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
           "<font color='darkred'><b>Cons</b></font>",
            styles["Heading2"],
        )
    )

    story.append(Spacer(1, 5))
 
    if len(cons) == 0:
        story.append(
            Paragraph(
               "<i>✓ No major weaknesses identified based on current financial metrics.</i>",
                styles["BodyText"],
            )
        )
    else:
        for c in cons:
            story.append(
                Paragraph(
                   f"• {c}",
                   styles["BodyText"],
               )
            )

    story.append(Spacer(1,15))



#----------------------------
# PAGE 2
# ----------------------------

    story.append(
        Paragraph(
           "<b>Financial Strength Radar</b>",
            styles["Heading2"],
        )
    )

    story.append(Spacer(1,10))

    story.append(
        Image(
           radar_chart,
           width=360,
           height=360,
        )
    )

    story.append(Spacer(1,20))

    
    story.append(PageBreak())

# ----------------------------
# Peer Comparison
# ----------------------------

    story.append(
        Paragraph(
            "<b>Peer Comparison</b>",
            styles["Heading1"],
        )
    )

    story.append(Spacer(1,10))

    peer_data = [
        [
           "Rank",
           "Company",
           "ROCE",
           "ROE",
           "NPM",
           "D/E",
        ]
    ]

    for rank, (_, row) in enumerate(peers.iterrows(), start=1):

        peer_data.append(
           [
            rank,
            row["company_name"],
            f"{row['roce_percentage']:.2f}%",
            f"{row['roe_percentage']:.2f}%",
            f"{row['net_profit_margin_pct']:.2f}%",
            f"{row['debt_to_equity']:.2f}",
           ]
       )

    peer_table = Table(
        peer_data,
        colWidths=[40,170,60,60,60,60]
    )

    peer_table.setStyle(
        TableStyle(
           [

            ("BACKGROUND",(0,0),(-1,0),colors.darkblue),
            ("TEXTCOLOR",(0,0),(-1,0),colors.white),

            ("GRID",(0,0),(-1,-1),0.5,colors.grey),

            ("ALIGN",(1,1),(-1,-1),"CENTER"),

            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

            ("BOTTOMPADDING",(0,0),(-1,0),8),

            ("BACKGROUND",(0,1),(-1,-1),colors.beige),

           ]
        )
    )

# Highlight current company

    for i, row in enumerate(peers.itertuples(), start=1):

        if i == 1:
            peer_table.setStyle(
                TableStyle(
               [
                   ("BACKGROUND", (0, i), (-1, i), colors.lightgreen),
                   ("FONTNAME", (0, i), (-1, i), "Helvetica-Bold"),
               ]
            )
        )
   
        if row.company_id == company_id:

            peer_table.setStyle(
                TableStyle(
                   [
                    ("BACKGROUND",(0,i),(-1,i),colors.lightblue),
                    ("FONTNAME",(0,i),(-1,i),"Helvetica-Bold"),
                   ]
                )
            )

    story.append(peer_table)

    story.append(Spacer(1,25))


    story.append(
        Paragraph(
           "<b>Cash Flow Analysis</b>",
            styles["Heading1"],
        )
    )

    story.append(Spacer(1, 15))


# ----------------------------
# Latest Cash Flow Chart
# ----------------------------

    latest_cf = cashflow.sort_values("year").iloc[-1]

    labels = [
        "CFO",
        "CFI",
        "CFF",
    ]

    values = [
        latest_cf["operating_activity"],
        latest_cf["investing_activity"],
        latest_cf["financing_activity"],
    ]

    plt.figure(figsize=(6,3))

    bars = plt.bar(
        labels,
        values,
    )

# Green for positive, red for negative
    for bar, value in zip(bars, values):
        if value >= 0:
           bar.set_color("green")
        else:
           bar.set_color("red")

    plt.title("Latest Year Cash Flow")
    plt.ylabel("₹ Cr")

    cashflow_chart = os.path.join(
        CHART_FOLDER,
        f"{company_id}_cashflow.png",
    )

    plt.tight_layout()
    plt.savefig(cashflow_chart)
    plt.close()

    story.append(
        Image(
          cashflow_chart,
          width=400,
          height=220,
        )
    )

    story.append(Spacer(1,20))

# ----------------------------
# Stock Price Performance
# ----------------------------

    story.append(PageBreak())

    story.append(
        Paragraph(
           "<b>Stock Price Performance</b>",
           styles["Heading1"],
        )
    )

    story.append(Spacer(1, 10))

    stock_price["date"] = pd.to_datetime(stock_price["date"])

    plt.figure(figsize=(8, 3))

    plt.plot(
       stock_price["date"],
       stock_price["close_price"],
       linewidth=2,
    )

    plt.title("Historical Closing Price")
    plt.xlabel("Year")
    plt.ylabel("Price (₹)")

    price_chart = os.path.join(
       CHART_FOLDER,
       f"{company_id}_price.png",
    )

    plt.tight_layout()
    plt.savefig(price_chart)
    plt.close()

    story.append(
        Image(
           price_chart,
           width=450,
           height=220,
        )
    )

    story.append(Spacer(1, 20))

    latest_val = valuation.sort_values("year").iloc[-1]

    #valuation logic

    if latest_val["pe_ratio"] < 20:
        valuation_label = "Undervalued"

    elif latest_val["pe_ratio"] < 40:
        valuation_label = "Fairly Valued"

    else:
        valuation_label = "Expensive"

    #create valuation table
    story.append(PageBreak())

    story.append(
        Paragraph(
           "<b>Valuation Dashboard</b>",
           styles["Heading1"],
        )
    )

    story.append(Spacer(1, 12))

    valuation_data = [
        ["Market Cap", f"₹ {latest_val['market_cap_crore']:,.0f} Cr"],
        ["PE Ratio", f"{latest_val['pe_ratio']:.2f}"],
        ["PB Ratio", f"{latest_val['pb_ratio']:.2f}"],
        ["Dividend Yield", f"{latest_val['dividend_yield_pct']:.2f}%"],
        ["Valuation", valuation_label],
    ]


    #create table

    valuation_table = Table(
       valuation_data,
       colWidths=[180, 220],
    )

    valuation_table.setStyle(
        TableStyle(
            [
               ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
               ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#EAF2F8")),
               ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
               ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
               ("TOPPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )

    story.append(valuation_table)

    story.append(Spacer(1, 20))

    # ----------------------------
    # Build PDF
    # ----------------------------

    doc.build(story)

    print("Saved:", pdf_file)


def main():

    conn = sqlite3.connect(DB_PATH)

    companies = pd.read_sql(
        """
        SELECT id
        FROM companies
        ORDER BY company_name
        """,
        conn,
    )

    conn.close()

    print(f"Generating {len(companies)} company tearsheets...\n")

    for company_id in companies["id"]:

        try:

            create_tearsheet(company_id)

            print(f"✓ {company_id}")

        except Exception as e:

            print(f"✗ {company_id} -> {e}")


if __name__ == "__main__":
    main()


