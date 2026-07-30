import streamlit as st
import plotly.graph_objects as go


from utils.db import (
    get_peer_groups,
    get_peer_percentiles,
)

# --------------------------------------------------
# Load Data
# --------------------------------------------------
peer_groups = get_peer_groups()
peer_percentiles = get_peer_percentiles()

# --------------------------------------------------
# Page Title
# --------------------------------------------------
st.title("👥 Peer Comparison")

# --------------------------------------------------
# Peer Group Selector
# --------------------------------------------------
group = st.selectbox(
    "Select Peer Group",
    sorted(peer_groups["peer_group_name"].unique()),
)

# --------------------------------------------------
# Companies in Selected Group
# --------------------------------------------------
companies = peer_groups[peer_groups["peer_group_name"] == group]

company = st.selectbox(
    "Select Company",
    sorted(companies["company_id"].unique()),
)

# --------------------------------------------------
# Benchmark Company
# --------------------------------------------------
benchmark = companies[companies["is_benchmark"] == 1]

if not benchmark.empty:
    benchmark_company = benchmark.iloc[0]["company_id"]
else:
    benchmark_company = "N/A"

st.success(f"Selected Group : {group}")
st.success(f"Selected Company : {company}")
st.info(f"⭐ Benchmark Company : {benchmark_company}")

# --------------------------------------------------
# Radar Chart
# --------------------------------------------------
latest_year = peer_percentiles["year"].max()

metrics = {
    "return_on_equity_pct": "ROE (%)",
    "net_profit_margin_pct": "Net Profit Margin (%)",
    "debt_to_equity": "Debt / Equity",
    "interest_coverage": "Interest Coverage",
    "asset_turnover": "Asset Turnover",
    "free_cash_flow_cr": "Free Cash Flow",
}

company_data = peer_percentiles[
    (peer_percentiles["company_id"] == company)
    & (peer_percentiles["year"] == latest_year)
]

peer_data = peer_percentiles[
    (peer_percentiles["peer_group_name"] == group)
    & (peer_percentiles["year"] == latest_year)
]

peer_avg = peer_data.groupby("metric")["value"].mean().reset_index()

company_values = []
peer_values = []
labels = []

for metric, label in metrics.items():

    company_row = company_data[company_data["metric"] == metric]

    peer_row = peer_avg[peer_avg["metric"] == metric]

    if company_row.empty:
        company_values.append(0)
    else:
        company_values.append(company_row.iloc[0]["value"])

    if peer_row.empty:
        peer_values.append(0)
    else:
        peer_values.append(peer_row.iloc[0]["value"])

    labels.append(label)

# --------------------------------------------------
# Heading
# --------------------------------------------------
st.subheader(f"📊 {company} vs Peer Group Average")

# --------------------------------------------------
# Figure
# --------------------------------------------------
fig = go.Figure()

fig.add_trace(
    go.Scatterpolar(
        r=company_values,
        theta=labels,
        fill="toself",
        name=company,
        line=dict(width=3),
        opacity=0.7,
    )
)

fig.add_trace(
    go.Scatterpolar(
        r=peer_values,
        theta=labels,
        fill="toself",
        name="Peer Average",
        line=dict(width=3),
        opacity=0.6,
    )
)

fig.update_layout(
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(
        color="black",
        size=13,
    ),
    polar=dict(
        bgcolor="white",
        radialaxis=dict(
            visible=True,
            range=[0, 100],
            tickmode="linear",
            dtick=20,
            tickfont=dict(
                color="black",
                size=12,
            ),
            gridcolor="lightgray",
            linecolor="gray",
        ),
        angularaxis=dict(
            tickfont=dict(
                color="black",
                size=13,
            ),
            gridcolor="lightgray",
            linecolor="gray",
        ),
    ),
    legend=dict(
        orientation="h",
        x=0.5,
        xanchor="center",
        y=1.12,
        yanchor="bottom",
        font=dict(
            size=12,
            color="black",
        ),
    ),
    margin=dict(
        l=50,
        r=50,
        t=20,
        b=20,
    ),
    height=650,
)

st.plotly_chart(
    fig,
    use_container_width=True,
    config={"displayModeBar": False},
)


# --------------------------------------------------
# Peer Comparison Table
# --------------------------------------------------
st.divider()

st.subheader("Peer Comparison Table")

table = peer_percentiles[
    (peer_percentiles["peer_group_name"] == group)
    & (peer_percentiles["year"] == latest_year)
]

table = table.pivot(
    index="company_id",
    columns="metric",
    values="value",
).reset_index()

table = table.rename(
    columns={
        "company_id": "Company",
        "return_on_equity_pct": "ROE",
        "net_profit_margin_pct": "Net Profit Margin",
        "debt_to_equity": "Debt/Equity",
        "interest_coverage": "Interest Coverage",
        "asset_turnover": "Asset Turnover",
        "free_cash_flow_cr": "Free Cash Flow",
    }
)

# --------------------------------------------------
# Status Column
# --------------------------------------------------
table["Status"] = table["Company"].apply(
    lambda x: (
        "⭐ Benchmark"
        if x == benchmark_company
        else ("🔵 Selected" if x == company else "")
    )
)

# --------------------------------------------------
# Arrange Columns
# --------------------------------------------------
columns = [
    "Status",
    "Company",
    "ROE",
    "Net Profit Margin",
    "Debt/Equity",
    "Interest Coverage",
    "Asset Turnover",
    "Free Cash Flow",
]

columns = [c for c in columns if c in table.columns]

# --------------------------------------------------
# Round Numeric Columns
# --------------------------------------------------
numeric_cols = [
    "ROE",
    "Net Profit Margin",
    "Debt/Equity",
    "Interest Coverage",
    "Asset Turnover",
    "Free Cash Flow",
]

for col in numeric_cols:
    if col in table.columns:
        table[col] = table[col].round(2)

# --------------------------------------------------
# Display Table
# --------------------------------------------------
st.dataframe(
    table[columns],
    use_container_width=True,
    hide_index=True,
)
