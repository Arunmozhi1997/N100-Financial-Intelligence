import streamlit as st
import pandas as pd
import plotly.express as px

from utils.db import (
    get_companies,
    get_ratios,
    get_profit_loss,
    get_sectors,
    get_pros_cons,
)


# ----------------------------------------------------
# Helper Function
# ----------------------------------------------------
def safe_value(value, suffix=""):
    if (
        pd.isna(value)
        or value is None
        or str(value).strip().lower() in ["none", "nan", ""]
    ):
        return "N/A"
    return f"{value}{suffix}"


# ----------------------------------------------------
# Load Data
# ----------------------------------------------------
companies = get_companies()
ratios = get_ratios()
sectors = get_sectors()


# ----------------------------------------------------
# Page Title
# ----------------------------------------------------
st.title("🏢 Company Profile")


# ----------------------------------------------------
# Company Selector
# ----------------------------------------------------
company = st.selectbox(
    "Select Company",
    sorted(companies["id"].unique()),
)


# ----------------------------------------------------
# Load Selected Company Data
# ----------------------------------------------------
company_info = companies[companies["id"] == company]

sector_info = sectors[sectors["company_id"] == company]


company_ratios = ratios[ratios["company_id"] == company].sort_values("year")


profit_loss = get_profit_loss(company)

pros_cons = get_pros_cons(company)


# ----------------------------------------------------
# Company Information
# ----------------------------------------------------
st.subheader(company)


if not company_info.empty:

    info = company_info.iloc[0]

    col1, col2 = st.columns([1, 3])

    with col1:

        if (
            "company_logo" in company_info.columns
            and pd.notna(info["company_logo"])
            and str(info["company_logo"]).startswith("http")
        ):
            st.image(
                info["company_logo"],
                width=120,
            )

    with col2:

        st.write(f"### {info['company_name']}")

        if not sector_info.empty:

            sector = sector_info.iloc[0]

            st.write(f"**Sector:** {sector['broad_sector']}")

            st.write(f"**Sub Sector:** {sector['sub_sector']}")

        st.write(f"**Website:** {safe_value(info['website'])}")

        st.write(f"**Face Value:** {safe_value(info['face_value'])}")

        st.write(f"**Book Value:** {safe_value(info['book_value'])}")

        st.markdown("### About Company")

        st.write(safe_value(info["about_company"]))


# ----------------------------------------------------
# KPI Cards
# ----------------------------------------------------
if not company_ratios.empty:

    latest = company_ratios.iloc[-1]

    st.markdown("## Latest KPIs")

    c1, c2, c3 = st.columns(3)

    c1.metric("ROE", f"{latest['return_on_equity_pct']:.2f}%")

    c2.metric("Net Profit Margin", f"{latest['net_profit_margin_pct']:.2f}%")

    c3.metric("Debt / Equity", f"{latest['debt_to_equity']:.2f}")

    c4, c5, c6 = st.columns(3)

    c4.metric("Asset Turnover", f"{latest['asset_turnover']:.2f}")

    c5.metric("Interest Coverage", f"{latest['interest_coverage']:.2f}")

    c6.metric("Free Cash Flow", f"{latest['free_cash_flow_cr']:.2f} Cr")


# ----------------------------------------------------
# Revenue & Net Profit Chart
# ----------------------------------------------------
st.divider()

st.subheader("Revenue & Net Profit Trend")


if not profit_loss.empty:

    fig = px.line(
        profit_loss,
        x="year",
        y=[
            "sales",
            "net_profit",
        ],
        markers=True,
        title="Revenue vs Net Profit",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )


else:

    st.info("No Profit & Loss data available.")


# ----------------------------------------------------
# ROE Trend
# ----------------------------------------------------
st.divider()

st.subheader("ROE Trend")


if not company_ratios.empty:

    fig = px.line(
        company_ratios,
        x="year",
        y="return_on_equity_pct",
        markers=True,
        title="Return on Equity",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )


# ----------------------------------------------------
# Debt to Equity Trend
# ----------------------------------------------------
st.divider()

st.subheader("Debt to Equity Trend")


if not company_ratios.empty:

    fig = px.line(
        company_ratios,
        x="year",
        y="debt_to_equity",
        markers=True,
        title="Debt to Equity Ratio",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )


# ----------------------------------------------------
# Pros & Cons
# ----------------------------------------------------
st.divider()

st.subheader("Pros & Cons")


if not pros_cons.empty:

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### ✅ Pros")

        for pro in pros_cons["pros"].dropna():

            st.success(pro)

    with col2:

        st.markdown("### ❌ Cons")

        for con in pros_cons["cons"].dropna():

            st.error(con)


else:

    st.info("No Pros & Cons available.")


# ----------------------------------------------------
# Financial Ratios Table
# ----------------------------------------------------

st.divider()

st.subheader("Financial Ratios")

display_ratios = company_ratios.copy()

display_ratios = display_ratios.replace(
    [None, "None", "null", "NULL", "nan", ""], "N/A"
)

display_ratios = display_ratios.fillna("N/A")


st.dataframe(display_ratios, use_container_width=True, hide_index=True)


# ----------------------------------------------------
# Profit & Loss Table
# ----------------------------------------------------
st.divider()

st.subheader("Profit & Loss")

display_profit = profit_loss.copy()

display_profit = display_profit.fillna("N/A")
display_profit = display_profit.replace(
    [None, "None", "null", "NULL", "nan"],
    "N/A",
)


st.dataframe(
    display_profit,
    use_container_width=True,
)
