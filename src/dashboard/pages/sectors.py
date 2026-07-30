import streamlit as st
import plotly.express as px
import pandas as pd

from utils.db import get_sector_analysis

# --------------------------------------------------
# Load Data
# --------------------------------------------------
df = get_sector_analysis()

# --------------------------------------------------
# Page Title
# --------------------------------------------------
st.title("🏭 Sector Analysis")

if df.empty:
    st.warning("No sector data available.")
    st.stop()

# --------------------------------------------------
# Convert columns to proper data types
# --------------------------------------------------
df["year"] = pd.to_numeric(df["year"], errors="coerce")
df["sales"] = pd.to_numeric(df["sales"], errors="coerce")
df["return_on_equity_pct"] = pd.to_numeric(
    df["return_on_equity_pct"],
    errors="coerce",
)
df["market_cap_crore"] = pd.to_numeric(
    df["market_cap_crore"],
    errors="coerce",
)
df["net_profit_margin_pct"] = pd.to_numeric(
    df["net_profit_margin_pct"],
    errors="coerce",
)
df["debt_to_equity"] = pd.to_numeric(
    df["debt_to_equity"],
    errors="coerce",
)

df = df.dropna(subset=["year"])
df["year"] = df["year"].astype(int)

# --------------------------------------------------
# Latest Year
# --------------------------------------------------
latest_year = df["year"].max()

latest = df[df["year"] == latest_year]

# --------------------------------------------------
# Sector Selector
# --------------------------------------------------
sector = st.selectbox(
    "Select Broad Sector",
    sorted(latest["broad_sector"].dropna().unique()),
)

sector_df = latest[latest["broad_sector"] == sector].copy()

# Remove rows with missing chart values
sector_df = sector_df.dropna(
    subset=[
        "sales",
        "return_on_equity_pct",
        "market_cap_crore",
    ]
)

# --------------------------------------------------
# Debug Information
# --------------------------------------------------
st.write("Rows:", len(sector_df))

# --------------------------------------------------
# Bubble Chart
# --------------------------------------------------
st.subheader("Revenue vs ROE")

if sector_df.empty:

    st.warning("No valid data available for this sector.")

else:

    fig = px.scatter(
        sector_df,
        x="sales",
        y="return_on_equity_pct",
        size="market_cap_crore",
        color="sub_sector",
        hover_name="company_id",
        hover_data={
            "sales": True,
            "market_cap_crore": True,
            "return_on_equity_pct": True,
        },
        size_max=60,
        title=f"{sector} Companies",
    )

    fig.update_layout(
        xaxis_title="Revenue",
        yaxis_title="ROE (%)",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

# --------------------------------------------------
# Sector Median KPIs
# --------------------------------------------------
st.divider()

st.subheader("Sector Median KPIs")

if not sector_df.empty:

    median_df = (
        sector_df[
            [
                "return_on_equity_pct",
                "net_profit_margin_pct",
                "debt_to_equity",
            ]
        ]
        .median()
        .reset_index()
    )

    median_df.columns = [
        "Metric",
        "Median",
    ]

    fig = px.bar(
        median_df,
        x="Metric",
        y="Median",
        text="Median",
        title=f"{sector} Median KPIs",
    )

    fig.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

# --------------------------------------------------
# Company Table
# --------------------------------------------------
st.divider()

st.subheader("Companies")

if not sector_df.empty:

    display = sector_df[
        [
            "company_id",
            "sub_sector",
            "sales",
            "return_on_equity_pct",
            "net_profit_margin_pct",
            "debt_to_equity",
            "market_cap_crore",
        ]
    ].copy()

    display.columns = [
        "Company",
        "Sub Sector",
        "Revenue",
        "ROE (%)",
        "Net Profit Margin (%)",
        "Debt/Equity",
        "Market Cap (Cr)",
    ]

    st.dataframe(
        display,
        use_container_width=True,
        hide_index=True,
    )
