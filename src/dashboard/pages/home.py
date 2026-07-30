import streamlit as st
import plotly.express as px

from utils.db import (
    get_companies,
    get_ratios,
    get_sectors,
)

# -----------------------------------------
# Load Data
# -----------------------------------------
companies = get_companies()
ratios = get_ratios()
sectors = get_sectors()

# -----------------------------------------
# Sidebar
# -----------------------------------------
years = sorted(ratios["year"].dropna().astype(int).unique().tolist())


selected_year = st.sidebar.slider(
    "Select Financial Year",
    min_value=min(years),
    max_value=max(years),
    value=max(years),
    step=1,
)
st.sidebar.caption(f"Selected Year: {selected_year}")

latest = ratios[ratios["year"].astype(int) == selected_year].copy()


# -----------------------------------------
# KPI Calculations
# -----------------------------------------
total_companies = latest["company_id"].nunique()

median_roe = round(
    latest["return_on_equity_pct"].median(),
    2,
)

median_de = round(
    latest["debt_to_equity"].median(),
    2,
)

avg_npm = round(
    latest["net_profit_margin_pct"].mean(),
    2,
)

avg_asset_turnover = round(
    latest["asset_turnover"].mean(),
    2,
)

debt_free = (latest["debt_to_equity"] == 0).sum()

# -----------------------------------------
# Sector Summary
# -----------------------------------------
sector_counts = sectors.groupby("broad_sector").size().reset_index(name="Companies")

# -----------------------------------------
# Dashboard Title
# -----------------------------------------
st.title("📈 N100 Financial Intelligence Dashboard")

st.caption(f"Financial Year: {selected_year}")

# -----------------------------------------
# KPI Cards
# -----------------------------------------
c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Companies",
        total_companies,
    )

with c2:
    st.metric("Median ROE (%)", f"{median_roe:.2f}%")

with c3:
    st.metric("Median D/E", f"{median_de:.2f}")

c4, c5, c6 = st.columns(3)

with c4:
    st.metric("Average Net Profit Margin (%)", f"{avg_npm:.2f}%")

with c5:
    st.metric("Average Asset Turnover", f"{avg_asset_turnover:.2f}")

with c6:
    st.metric("Debt-Free Companies", debt_free)

# -----------------------------------------
# Sector Distribution
# -----------------------------------------
st.divider()

st.subheader("Sector Distribution")

fig = px.pie(
    sector_counts,
    names="broad_sector",
    values="Companies",
    hole=0.5,
    title="Companies by Broad Sector",
)

fig.update_traces(
    textposition="inside",
    textinfo="percent+label",
)

fig.update_layout(
    legend_title="Sector",
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

# -----------------------------------------
# Top 5 Companies by ROE
# -----------------------------------------
st.divider()

st.subheader("🏆 Top 5 Companies by ROE")

top5 = (
    latest[
        [
            "company_id",
            "return_on_equity_pct",
            "net_profit_margin_pct",
            "debt_to_equity",
            "asset_turnover",
        ]
    ]
    .merge(
        companies[
            [
                "id",
                "company_name",
            ]
        ],
        left_on="company_id",
        right_on="id",
        how="left",
    )
    .drop(columns="id")
    .sort_values(
        by="return_on_equity_pct",
        ascending=False,
    )
    .head(5)
)

top5 = top5.rename(
    columns={
        "company_id": "Ticker",
        "company_name": "Company Name",
        "return_on_equity_pct": "ROE (%)",
        "net_profit_margin_pct": "Net Profit Margin (%)",
        "debt_to_equity": "Debt/Equity",
        "asset_turnover": "Asset Turnover",
    }
)

st.dataframe(
    top5,
    use_container_width=True,
    hide_index=True,
)

# -----------------------------------------
# Latest Financial Ratios
# -----------------------------------------
st.divider()

st.subheader("Latest Financial Ratios")

display_df = latest[
    [
        "company_id",
        "return_on_equity_pct",
        "net_profit_margin_pct",
        "debt_to_equity",
        "interest_coverage",
        "asset_turnover",
        "free_cash_flow_cr",
    ]
].copy()

display_df.columns = [
    "Company",
    "ROE (%)",
    "Net Profit Margin (%)",
    "Debt/Equity",
    "Interest Coverage",
    "Asset Turnover",
    "Free Cash Flow (Cr)",
]

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
)
