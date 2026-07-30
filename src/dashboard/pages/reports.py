import streamlit as st
import pandas as pd

from utils.db import (
    get_companies,
    get_reports,
)

# --------------------------------------------------
# Load Data
# --------------------------------------------------
companies = get_companies()

st.title("📄 Annual Reports")

# --------------------------------------------------
# Company Selector
# --------------------------------------------------
company = st.selectbox("Select Company", sorted(companies["id"].unique()))

# --------------------------------------------------
# Company Details
# --------------------------------------------------
company_row = companies[companies["id"] == company]

if company_row.empty:
    st.error("Company not found.")
    st.stop()

company_name = company_row.iloc[0]["company_name"]

st.header(company_name)
st.caption(company)

# --------------------------------------------------
# Reports
# --------------------------------------------------
reports = get_reports(company)

if reports.empty:
    st.warning("No reports available.")
    st.stop()

reports = reports.dropna(subset=["year"])
reports["year"] = reports["year"].astype(int)

reports = reports.sort_values("year", ascending=False)

# --------------------------------------------------
# Status
# --------------------------------------------------
reports["Status"] = reports["annual_report"].apply(
    lambda x: (
        "Available"
        if (pd.notna(x) and str(x).strip().startswith("http"))
        else "Unavailable"
    )
)

available_reports = (reports["Status"] == "Available").sum()

missing_reports = (reports["Status"] == "Unavailable").sum()

coverage = round(
    available_reports / len(reports) * 100,
    1,
)

latest_year = reports["year"].max()

# --------------------------------------------------
# KPI Cards
# --------------------------------------------------
c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Latest Report",
    latest_year,
)

c2.metric(
    "Available Reports",
    available_reports,
)

c3.metric(
    "Missing Reports",
    missing_reports,
)

c4.metric("Coverage", f"{coverage}%")

st.divider()

# --------------------------------------------------
# Search Report Year
# --------------------------------------------------
st.subheader("🔍 Search Report Year")

search_year = st.text_input(
    "Enter Report Year",
    placeholder="e.g. 2024",
)

if search_year.strip():

    reports = reports[
        reports["year"]
        .astype(str)
        .str.contains(
            search_year.strip(),
            case=False,
            na=False,
        )
    ]

# --------------------------------------------------
# Annual Reports
# --------------------------------------------------
st.subheader("📚 Available Annual Reports")

for _, row in reports.iterrows():

    year = int(row["year"])

    url = str(row["annual_report"]).strip()

    with st.container(border=True):

        left, right = st.columns([2, 1])

        with left:

            st.markdown(f"### 📄 {year}")

            if row["Status"] == "Available":
                st.success("Available")
            else:
                st.error("Report unavailable")

        with right:

            if row["Status"] == "Available":

                st.link_button(
                    "Open PDF",
                    url,
                    use_container_width=True,
                )

st.divider()

# --------------------------------------------------
# Summary Table
# --------------------------------------------------
st.subheader("📋 Report Summary")

summary = reports[
    [
        "year",
        "Status",
        "annual_report",
    ]
].copy()

summary["annual_report"] = (
    summary["annual_report"]
    .replace(["Null", "NULL", "null", "None", "nan"], "N/A")
    .fillna("N/A")
)

summary.columns = [
    "Year",
    "Status",
    "Report URL",
]


st.dataframe(
    summary,
    use_container_width=True,
    hide_index=True,
)

# --------------------------------------------------
# Download
# --------------------------------------------------
summary["Report URL"] = summary["Report URL"].fillna("N/A")

csv = summary.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇ Download Report Summary",
    data=csv,
    file_name=f"{company}_reports.csv",
    mime="text/csv",
)
