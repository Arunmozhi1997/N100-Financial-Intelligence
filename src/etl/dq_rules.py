import pandas as pd


# -----------------------------
# DQ-08 Year Validation
# -----------------------------
def check_year_format(conn, table):

    try:

        df = pd.read_sql_query(
            f"SELECT year FROM {table}",
            conn
        )

        # Ignore NULL years (TTM rows)
        df = df[df["year"].notna()]

        invalid = df[
            ~df["year"]
            .astype(int)
            .astype(str)
            .str.match(r"^\d{4}$")
        ]

        return len(invalid)

    except Exception:
        return 0



# -----------------------------
# DQ-09 Negative Value Check
# -----------------------------

def check_negative_values(conn, table):

    df = pd.read_sql_query(
        f"SELECT * FROM {table}",
        conn
    )

    # Tables where negative values are expected
    allowed_tables = {
        "cashflow",
        "profitandloss",
        "financial_ratios",
    }

    if table in allowed_tables:
        return 0

    numeric = df.select_dtypes(include="number")

    negative = (numeric < 0).sum().sum()

    return int(negative)



# -----------------------------
# DQ-10 Percentage Range
# -----------------------------

def check_percentage_range(conn, table):

    df = pd.read_sql_query(
        f"SELECT * FROM {table}",
        conn
    )

    issues = 0

    # Only validate tax percentage
    if "tax_percentage" in df.columns:

        issues += (
            df["tax_percentage"] > 100
        ).sum()

    # Validate ROE
    if "roe_percentage" in df.columns:

        issues += (
            (df["roe_percentage"] < -100) |
            (df["roe_percentage"] > 100)
        ).sum()

    # Validate ROCE
    if "roce_percentage" in df.columns:

        issues += (
            (df["roce_percentage"] < -100) |
            (df["roce_percentage"] > 100)
        ).sum()

    return issues

# -----------------------------
# DQ-11 Empty Table Check
# -----------------------------

def check_empty_table(conn, table):

    count = pd.read_sql_query(
        f"SELECT COUNT(*) c FROM {table}",
        conn
    )


    return count.iloc[0]["c"] == 0