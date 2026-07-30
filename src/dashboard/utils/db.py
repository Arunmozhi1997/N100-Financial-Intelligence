import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

# --------------------------------------------------
# Database Path
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[3]
DB_PATH = BASE_DIR / "db" / "nifty100.db"


# --------------------------------------------------
# Database Connection
# --------------------------------------------------
def get_connection():
    """Return SQLite connection."""
    return sqlite3.connect(DB_PATH)


# --------------------------------------------------
# Companies
# --------------------------------------------------
@st.cache_data(ttl=600)
def get_companies():

    conn = get_connection()

    query = """
    SELECT *
    FROM companies
    ORDER BY company_name
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


# --------------------------------------------------
# Financial Ratios
# --------------------------------------------------
@st.cache_data(ttl=600)
def get_ratios():

    conn = get_connection()

    query = """
    SELECT *
    FROM financial_ratios
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


# --------------------------------------------------
# Sectors
# --------------------------------------------------
@st.cache_data(ttl=600)
def get_sectors():

    conn = get_connection()

    query = """
    SELECT *
    FROM sectors
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


# --------------------------------------------------
# Profit & Loss
# --------------------------------------------------
@st.cache_data(ttl=600)
def get_profit_loss(ticker):

    conn = get_connection()

    query = """
    SELECT *
    FROM profitandloss
    WHERE company_id = ?
      AND year IS NOT NULL
    ORDER BY CAST(year AS INTEGER)
    """

    df = pd.read_sql(
        query,
        conn,
        params=[ticker],
    )

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_latest_ratios():
    conn = get_connection()

    query = """
    SELECT *
    FROM financial_ratios
    WHERE year = (
        SELECT MAX(year)
        FROM financial_ratios
    )
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_pros_cons(ticker):
    conn = get_connection()

    query = """
    SELECT *
    FROM prosandcons
    WHERE company_id=?
    """

    df = pd.read_sql(query, conn, params=[ticker])

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_peer_groups():

    conn = get_connection()

    query = """
    SELECT *
    FROM peer_groups
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_peer_percentiles():

    conn = get_connection()

    query = """
    SELECT *
    FROM peer_percentiles
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


@st.cache_data(ttl=0)
def get_trends(ticker):

    conn = get_connection()

    query = """
    SELECT
        p.company_id,
        CAST(p.year AS INTEGER) AS year,
        p.sales,
        p.operating_profit,
        p.net_profit,

        r.return_on_equity_pct,
        r.net_profit_margin_pct,
        r.debt_to_equity,
        r.asset_turnover,
        r.free_cash_flow_cr

    FROM profitandloss p

    LEFT JOIN financial_ratios r
        ON TRIM(p.company_id) = TRIM(r.company_id)
       AND CAST(p.year AS INTEGER) = CAST(r.year AS INTEGER)

    WHERE TRIM(p.company_id) = TRIM(?)

    ORDER BY CAST(p.year AS INTEGER)
    """

    df = pd.read_sql(
        query,
        conn,
        params=[ticker],
    )

    # Remove rows without a valid year
    df = df.dropna(subset=["year"])

    # Convert year to integer
    df["year"] = df["year"].astype(int)

    # Remove duplicate years if any
    df = df.drop_duplicates(subset=["year"])

    # Sort by year
    df = df.sort_values("year")

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_sector_analysis():

    conn = get_connection()

    query = """
    SELECT
        s.company_id,
        s.broad_sector,
        s.sub_sector,
        p.year,
        p.sales,
        r.return_on_equity_pct,
        r.net_profit_margin_pct,
        r.debt_to_equity,
        m.market_cap_crore
    FROM sectors s

    LEFT JOIN profitandloss p
        ON s.company_id = p.company_id

    LEFT JOIN financial_ratios r
        ON s.company_id = r.company_id
        AND CAST(p.year AS INTEGER) = r.year

    LEFT JOIN market_cap m
        ON s.company_id = m.company_id
        AND CAST(p.year AS INTEGER) = m.year

    ORDER BY
        s.broad_sector,
        p.year
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_capital_data():

    conn = get_connection()

    query = """
    SELECT
        r.company_id,
        r.year,
        r.return_on_equity_pct,
        r.debt_to_equity,
        r.free_cash_flow_cr,
        r.capex_cr,
        r.dividend_payout_ratio_pct
    FROM financial_ratios r
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_reports(company):

    conn = get_connection()

    query = """
    SELECT
        company_id,
        year,
        annual_report
    FROM documents
    WHERE company_id = ?
    ORDER BY year DESC
    """

    df = pd.read_sql(
        query,
        conn,
        params=[company],
    )

    conn.close()

    return df
