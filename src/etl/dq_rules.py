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

        invalid = df[
            ~df["year"]
            .astype(str)
            .str.match(r"^\d{4}$")
        ]


        return len(invalid)


    except:
        return 0



# -----------------------------
# DQ-09 Negative Value Check
# -----------------------------

def check_negative_values(conn, table):

    df = pd.read_sql_query(
        f"SELECT * FROM {table}",
        conn
    )


    numeric = df.select_dtypes(
        include="number"
    )


    negative = (
        numeric < 0
    ).sum().sum()


    return negative



# -----------------------------
# DQ-10 Percentage Range
# -----------------------------

def check_percentage_range(conn, table):

    df = pd.read_sql_query(
        f"SELECT * FROM {table}",
        conn
    )


    columns = [
        c for c in df.columns
        if "pct" in c
        or "percentage" in c
    ]


    issues = 0


    for col in columns:

        issues += (
            (df[col] < -100)
            |
            (df[col] > 100)
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