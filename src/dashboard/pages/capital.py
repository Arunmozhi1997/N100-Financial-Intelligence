import streamlit as st
import plotly.express as px
import pandas as pd

from utils.db import get_capital_data

# --------------------------------------------------
# Load Data
# --------------------------------------------------
df = get_capital_data()

st.title("🏦 Capital Allocation Map")

if df.empty:
    st.warning("No capital allocation data available.")
    st.stop()

# --------------------------------------------------
# Data Cleaning
# --------------------------------------------------
df["year"] = pd.to_numeric(df["year"], errors="coerce")
df = df.dropna(subset=["year"])
df["year"] = df["year"].astype(int)

latest_year = df["year"].max()

latest = df[df["year"] == latest_year].copy()

# Fill missing values
cols = [
    "return_on_equity_pct",
    "debt_to_equity",
    "free_cash_flow_cr",
    "capex_cr",
    "dividend_payout_ratio_pct",
]

for col in cols:
    latest[col] = pd.to_numeric(latest[col], errors="coerce").fillna(0)

# --------------------------------------------------
# Capital Allocation Pattern
# --------------------------------------------------
latest["Pattern"] = "Stable"

latest.loc[
    latest["debt_to_equity"] >= 2,
    "Pattern",
] = "Debt Heavy"

latest.loc[
    latest["dividend_payout_ratio_pct"] >= 40,
    "Pattern",
] = "Dividend"

latest.loc[
    latest["capex_cr"] >= latest["capex_cr"].quantile(0.75),
    "Pattern",
] = "Capital Intensive"

latest.loc[
    (latest["free_cash_flow_cr"] > 0) & (latest["return_on_equity_pct"] >= 15),
    "Pattern",
] = "Cash Generator"

latest.loc[
    (latest["return_on_equity_pct"] >= 20) & (latest["debt_to_equity"] <= 0.5),
    "Pattern",
] = "Quality"

latest.loc[
    (latest["return_on_equity_pct"] >= 15) & (latest["free_cash_flow_cr"] < 0),
    "Pattern",
] = "Growth"

latest.loc[
    (latest["return_on_equity_pct"] < 10) & (latest["free_cash_flow_cr"] < 0),
    "Pattern",
] = "Turnaround"

# --------------------------------------------------
# Treemap Size
# --------------------------------------------------
latest["Treemap Size"] = latest["free_cash_flow_cr"].abs()

latest["Treemap Size"] = latest["Treemap Size"].fillna(1).clip(lower=1)

# Better names for hover labels
latest = latest.rename(
    columns={
        "return_on_equity_pct": "ROE",
        "debt_to_equity": "Debt/Equity",
        "free_cash_flow_cr": "Free Cash Flow",
        "capex_cr": "CAPEX",
        "dividend_payout_ratio_pct": "Dividend Payout",
    }
)

treemap_df = latest.dropna(
    subset=[
        "company_id",
        "Pattern",
        "Treemap Size",
    ]
)

# --------------------------------------------------
# Debug
# --------------------------------------------------
st.write(f"Companies : {len(treemap_df)}")

# --------------------------------------------------
# Treemap
# --------------------------------------------------
st.subheader("Capital Allocation Patterns")

fig = px.treemap(
    treemap_df,
    path=["Pattern", "company_id"],
    values="Treemap Size",
    color="ROE",
    color_continuous_scale="RdYlGn",
    range_color=(0, 30),
    hover_name="company_id",
    hover_data={
        "ROE": ":.2f",
        "Debt/Equity": ":.2f",
        "Free Cash Flow": ":,.0f",
        "CAPEX": ":,.0f",
        "Dividend Payout": ":.2f",
        "Treemap Size": False,
    },
)

fig.update_traces(textinfo="label")

fig.update_layout(
    margin=dict(
        t=40,
        l=10,
        r=10,
        b=10,
    )
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

# --------------------------------------------------
# Pattern Explorer
# --------------------------------------------------
st.divider()

st.subheader("📂 Explore Capital Allocation Pattern")

pattern = st.selectbox(
    "Choose Capital Allocation Pattern",
    sorted(treemap_df["Pattern"].unique()),
)

filtered = treemap_df[treemap_df["Pattern"] == pattern].sort_values(
    "ROE", ascending=False
)

st.success(f"{len(filtered)} companies found in '{pattern}'.")

# --------------------------------------------------
# Company Table
# --------------------------------------------------
display = filtered[
    [
        "company_id",
        "ROE",
        "Debt/Equity",
        "Free Cash Flow",
        "CAPEX",
        "Dividend Payout",
    ]
].copy()

display.rename(
    columns={
        "company_id": "Company",
        "ROE": "ROE (%)",
        "Debt/Equity": "Debt / Equity",
        "Free Cash Flow": "Free Cash Flow (Cr)",
        "CAPEX": "CAPEX (Cr)",
        "Dividend Payout": "Dividend Payout (%)",
    },
    inplace=True,
)

st.dataframe(
    display,
    use_container_width=True,
    hide_index=True,
)
