import streamlit as st

from utils.db import (
    get_companies,
    get_ratios,
)

st.title("🔎 Financial Screener")


companies = get_companies()
ratios = get_ratios()


latest_year = ratios["year"].max()


latest = ratios[ratios["year"] == latest_year]


# -----------------------------------------
# Sidebar Filters
# -----------------------------------------
st.sidebar.header("Filters")


roe = st.sidebar.slider(
    "Minimum ROE (%)",
    0,
    50,
    15,
)


de = st.sidebar.slider(
    "Maximum Debt/Equity",
    0.0,
    5.0,
    1.0,
)


fcf = st.sidebar.number_input(
    "Minimum Free Cash Flow",
    value=0.0,
)


interest = st.sidebar.slider(
    "Minimum Interest Coverage",
    0.0,
    100.0,
    1.0,
)


npm = st.sidebar.slider(
    "Minimum Net Profit Margin (%)",
    0.0,
    100.0,
    10.0,
)


asset = st.sidebar.slider(
    "Minimum Asset Turnover",
    0.0,
    5.0,
    0.5,
)


# -----------------------------------------
# Apply Filters
# -----------------------------------------
filtered = latest[
    (latest["return_on_equity_pct"] >= roe)
    & (latest["debt_to_equity"] <= de)
    & (latest["free_cash_flow_cr"] >= fcf)
    & (latest["interest_coverage"] >= interest)
    & (latest["net_profit_margin_pct"] >= npm)
    & (latest["asset_turnover"] >= asset)
]

# -----------------------------------------
# Merge Company Names
# -----------------------------------------
result = filtered.merge(
    companies,
    left_on="company_id",
    right_on="id",
    how="left",
)

# -----------------------------------------
# Results
# -----------------------------------------
st.metric(
    "Matching Companies",
    len(result),
)

if result.empty:

    st.warning("No companies match the selected filters.")

else:

    display = result[
        [
            "company_id",
            "company_name",
            "return_on_equity_pct",
            "debt_to_equity",
            "free_cash_flow_cr",
            "interest_coverage",
            "net_profit_margin_pct",
            "asset_turnover",
        ]
    ].copy()

    display.columns = [
        "Ticker",
        "Company",
        "ROE (%)",
        "Debt / Equity",
        "Free Cash Flow (Cr)",
        "Interest Coverage",
        "Net Profit Margin (%)",
        "Asset Turnover",
    ]

    st.dataframe(
        display,
        use_container_width=True,
        hide_index=True,
    )

    csv = display.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Download CSV",
        data=csv,
        file_name="screener.csv",
        mime="text/csv",
    )
