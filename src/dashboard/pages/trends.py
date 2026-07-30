import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from utils.db import (
    get_companies,
    get_trends,
)

# --------------------------------------------------
# Load Data
# --------------------------------------------------
companies = get_companies()

# --------------------------------------------------
# Page Title
# --------------------------------------------------
st.title("📈 Trend Analysis")

# --------------------------------------------------
# Company Selector
# --------------------------------------------------
company = st.selectbox(
    "Select Company",
    sorted(companies["id"].unique()),
)

trend = get_trends(company)

if trend.empty:
    st.warning("No trend data available.")
    st.stop()

# --------------------------------------------------
# Clean Data
# --------------------------------------------------
trend["year"] = pd.to_numeric(trend["year"], errors="coerce")

metric_columns = [
    "sales",
    "operating_profit",
    "net_profit",
    "return_on_equity_pct",
    "net_profit_margin_pct",
    "debt_to_equity",
    "asset_turnover",
    "free_cash_flow_cr",
]

for col in metric_columns:
    if col in trend.columns:
        trend[col] = pd.to_numeric(trend[col], errors="coerce")

trend = trend.sort_values("year")

# --------------------------------------------------
# Metric Selector
# --------------------------------------------------
metric_options = {
    "Sales": "sales",
    "Operating Profit": "operating_profit",
    "Net Profit": "net_profit",
    "ROE (%)": "return_on_equity_pct",
    "Net Profit Margin (%)": "net_profit_margin_pct",
    "Debt / Equity": "debt_to_equity",
    "Asset Turnover": "asset_turnover",
    "Free Cash Flow (Cr)": "free_cash_flow_cr",
}

selected_metrics = st.multiselect(
    "Select up to 3 Metrics",
    options=list(metric_options.keys()),
    default=["Sales"],
    max_selections=3,
)

# --------------------------------------------------
# Trend Chart
# --------------------------------------------------
if selected_metrics:

    fig = go.Figure()

    plotted = False

    for metric in selected_metrics:

        column = metric_options[metric]

        if column not in trend.columns:
            continue

        temp = trend[["year", column]].dropna()

        if temp.empty:
            continue

        plotted = True

        temp["YoY"] = temp[column].pct_change().mul(100).round(2)

        hover_text = []

        for _, row in temp.iterrows():

            if pd.isna(row["YoY"]):
                yoy = "N/A"
            else:
                yoy = f"{row['YoY']:.2f}%"

            hover_text.append(
                f"<b>Year:</b> {int(row['year'])}"
                f"<br><b>{metric}:</b> {row[column]:,.2f}"
                f"<br><b>YoY Growth:</b> {yoy}"
            )

        fig.add_trace(
            go.Scatter(
                x=temp["year"],
                y=temp[column],
                mode="lines+markers",
                name=metric,
                line=dict(width=3),
                marker=dict(size=8),
                hovertext=hover_text,
                hoverinfo="text",
            )
        )

    if plotted:

        fig.update_layout(
            title=dict(
                text=f"{company} Financial Trend Analysis",
                x=0.5,
            ),
            template="plotly_white",
            height=650,
            hovermode="x unified",
            xaxis=dict(
                title="Financial Year",
                dtick=1,
                showgrid=True,
            ),
            yaxis=dict(
                title="Metric Value",
                showgrid=True,
            ),
            legend=dict(
                orientation="h",
                y=1.10,
                x=0.5,
                xanchor="center",
            ),
            margin=dict(
                l=40,
                r=40,
                t=80,
                b=40,
            ),
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    else:
        st.warning("No data available for selected metrics.")

# --------------------------------------------------
# YoY Table
# --------------------------------------------------
st.divider()

st.subheader("📊 Year-over-Year Growth")


growth = trend.copy()

for column in metric_options.values():

    if column in growth.columns:

        growth[f"{column}_YoY"] = growth[column].pct_change().mul(100).round(2)

display_columns = ["year"]

for metric in selected_metrics:

    column = metric_options[metric]

    display_columns.extend(
        [
            column,
            f"{column}_YoY",
        ]
    )


display_growth = growth[display_columns].copy()

for col in display_growth.columns:
    if col.endswith("_YoY"):
        display_growth[col] = display_growth[col].replace({None: "N/A"})
        display_growth[col] = display_growth[col].fillna("N/A")


display_growth.columns = [
    col.replace("return_on_equity_pct", "ROE")
    .replace("net_profit_margin_pct", "Net Profit Margin")
    .replace("debt_to_equity", "Debt / Equity")
    .replace("asset_turnover", "Asset Turnover")
    .replace("free_cash_flow_cr", "Free Cash Flow")
    .replace("_YoY", " YoY (%)")
    .replace("sales", "Sales")
    .replace("operating_profit", "Operating Profit")
    .replace("net_profit", "Net Profit")
    .replace("year", "Year")
    for col in display_growth.columns
]

st.dataframe(
    display_growth,
    use_container_width=True,
    hide_index=True,
)
