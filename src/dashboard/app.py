from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# ----------------------------------------
# Page Config
# ----------------------------------------
st.set_page_config(
    page_title="N100 Financial Intelligence",
    page_icon="📈",
    layout="wide",
)

# ----------------------------------------
# Paths
# ----------------------------------------
BASE_DIR = Path(__file__).resolve().parents[2]
OUTPUT_DIR = BASE_DIR / "output"

# ----------------------------------------
# Title
# ----------------------------------------
st.title("📈 N100 Financial Intelligence")
st.markdown("### Stock Screening Dashboard")

# ----------------------------------------
# Screeners
# ----------------------------------------
screeners = {
    "Quality Compounder": "quality_compounder.xlsx",
    "Value Pick": "value_pick.xlsx",
    "Growth Accelerator": "growth_accelerator.xlsx",
    "Dividend Champion": "dividend_champion.xlsx",
    "Debt Free Blue Chip": "debt_free_blue_chip.xlsx",
    "Turnaround Watch": "turnaround_watch.xlsx",
}

selected = st.sidebar.selectbox(
    "Select Screener",
    list(screeners.keys())
)

file = OUTPUT_DIR / screeners[selected]

# ----------------------------------------
# Load Excel
# ----------------------------------------
if not file.exists():
    st.error(f"{file.name} not found.")
    st.stop()

df = pd.read_excel(file)

# ----------------------------------------
# Sidebar Filters
# ----------------------------------------
st.sidebar.header("Filters")

years = sorted(df["year"].dropna().unique().tolist())
selected_year = st.sidebar.selectbox(
    "Year",
    ["All"] + years
)

companies = sorted(df["company_name"].dropna().unique().tolist())
selected_company = st.sidebar.selectbox(
    "Company",
    ["All"] + companies
)

search = st.sidebar.text_input("Search Company")

# ----------------------------------------
# Apply Filters
# ----------------------------------------
filtered = df.copy()

if selected_year != "All":
    filtered = filtered[filtered["year"] == selected_year]

if selected_company != "All":
    filtered = filtered[
        filtered["company_name"] == selected_company
    ]

if search:
    filtered = filtered[
        filtered["company_name"].str.contains(
            search,
            case=False,
            na=False,
        )
    ]

# ----------------------------------------
# KPI Cards
# ----------------------------------------
st.subheader(selected)

c1, c2, c3 = st.columns(3)

c1.metric(
    "Companies",
    len(filtered)
)

if "return_on_equity_pct" in filtered.columns:
    c2.metric(
        "Average ROE",
        f"{filtered['return_on_equity_pct'].mean():.2f}%"
    )

if "debt_to_equity" in filtered.columns:
    c3.metric(
        "Average Debt/Equity",
        f"{filtered['debt_to_equity'].mean():.2f}"
    )

st.divider()

# ----------------------------------------
# Charts
# ----------------------------------------

left, right = st.columns(2)

# Top ROE
if "return_on_equity_pct" in filtered.columns:

    chart_df = (
        filtered.sort_values(
            "return_on_equity_pct",
            ascending=False
        )
        .head(10)
    )

    fig = px.bar(
        chart_df,
        x="company_name",
        y="return_on_equity_pct",
        title="Top 10 Companies by ROE",
        text_auto=".2f",
    )

    left.plotly_chart(
        fig,
        use_container_width=True
    )

# Debt Equity
if "debt_to_equity" in filtered.columns:

    fig2 = px.histogram(
        filtered,
        x="debt_to_equity",
        nbins=20,
        title="Debt to Equity Distribution",
    )

    right.plotly_chart(
        fig2,
        use_container_width=True
    )

# ----------------------------------------
# Free Cash Flow
# ----------------------------------------

if "free_cash_flow_cr" in filtered.columns:

    chart_df = (
        filtered.sort_values(
            "free_cash_flow_cr",
            ascending=False
        )
        .head(10)
    )

    fig3 = px.bar(
        chart_df,
        x="company_name",
        y="free_cash_flow_cr",
        title="Top Free Cash Flow",
        text_auto=".2f",
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

# ----------------------------------------
# Data Table
# ----------------------------------------

st.subheader("Screening Results")

st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True,
)

# ----------------------------------------
# Download
# ----------------------------------------

st.download_button(
    label="⬇ Download Filtered Data",
    data=filtered.to_csv(index=False),
    file_name="screening_results.csv",
    mime="text/csv",
)