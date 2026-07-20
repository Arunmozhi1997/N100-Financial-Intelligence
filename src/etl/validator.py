"""
validator.py

Runs data quality checks on Nifty100 SQLite database.
"""

import sqlite3
from pathlib import Path
import pandas as pd

# Import DQ rule functions
from src.etl.dq_rules import (
    check_year_format,
    check_negative_values,
    check_percentage_range,
    check_empty_table,
)


# Store validation results
VALIDATION_RESULTS = []


BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "db" / "nifty100.db"

REPORT_PATH = BASE_DIR / "reports" / "validation_failures.csv"



def get_connection():

    return sqlite3.connect(DB_PATH)



# -----------------------------
# DQ-01 Null Value Check
# -----------------------------

def check_null_values(conn, table):

    df = pd.read_sql_query(
        f"SELECT * FROM {table}",
        conn
    )

    nulls = df.isnull().sum()

    result = nulls[nulls > 0]


    VALIDATION_RESULTS.append(
        {
            "rule": "DQ-01",
            "table": table,
            "status": "FAIL" if len(result) > 0 else "PASS",
            "issue": str(result.to_dict()) if len(result) > 0 else ""
        }
    )


    return result



# -----------------------------
# DQ-02 Duplicate Check
# -----------------------------

def check_duplicates(conn, table):

    df = pd.read_sql_query(
        f"SELECT * FROM {table}",
        conn
    )


    duplicates = df.duplicated().sum()


    VALIDATION_RESULTS.append(
        {
            "rule": "DQ-02",
            "table": table,
            "status": "FAIL" if duplicates > 0 else "PASS",
            "issue": f"{duplicates} duplicate rows"
        }
    )


    return duplicates



# -----------------------------
# DQ-03 Primary Key Check
# -----------------------------

def check_primary_key(conn, table, column):

    query = f"""
    SELECT {column}, COUNT(*) as count
    FROM {table}
    GROUP BY {column}
    HAVING COUNT(*) > 1
    """

    result = pd.read_sql_query(
        query,
        conn
    )


    VALIDATION_RESULTS.append(
        {
            "rule": "DQ-03",
            "table": table,
            "status": "FAIL" if len(result) > 0 else "PASS",
            "issue": "Duplicate primary keys" if len(result) > 0 else ""
        }
    )


    return result



# -----------------------------
# DQ-04 Foreign Key Check
# -----------------------------

def check_foreign_keys(conn, table):

    query = f"""
    SELECT *
    FROM {table}
    WHERE company_id NOT IN
    (
        SELECT id FROM companies
    )
    """

    result = pd.read_sql_query(
        query,
        conn
    )


    VALIDATION_RESULTS.append(
        {
            "rule": "DQ-04",
            "table": table,
            "status": "FAIL" if len(result) > 0 else "PASS",
            "issue": f"{len(result)} invalid company IDs"
        }
    )


    return result



# -----------------------------
# DQ-05 Row Count Check
# -----------------------------

def row_count(conn, table):

    result = pd.read_sql_query(
        f"SELECT COUNT(*) as count FROM {table}",
        conn
    )

    return result.iloc[0]["count"]



# -----------------------------
# DQ-06 Required Column Check
# -----------------------------

def check_required_columns(conn, table, required_columns):

    columns = pd.read_sql_query(
        f"PRAGMA table_info({table})",
        conn
    )["name"].tolist()


    missing = set(required_columns) - set(columns)


    VALIDATION_RESULTS.append(
        {
            "rule": "DQ-06",
            "table": table,
            "status": "FAIL" if missing else "PASS",
            "issue": f"Missing columns {missing}" if missing else ""
        }
    )


    return missing



# -----------------------------
# DQ-07 Data Type Check
# -----------------------------

def check_data_types(conn, table):

    df = pd.read_sql_query(
        f"SELECT * FROM {table}",
        conn
    )


    issues = []


    for column in df.columns:

        if df[column].dtype not in [
            "int64",
            "float64",
            "object"
        ]:

            issues.append(column)


    VALIDATION_RESULTS.append(
        {
            "rule": "DQ-07",
            "table": table,
            "status": "FAIL" if issues else "PASS",
            "issue": f"Invalid types: {issues}" if issues else ""
        }
    )


    return issues



# -----------------------------
# Validation Summary
# -----------------------------

def validation_summary():

    conn = get_connection()


    tables = [
        "companies",
        "profitandloss",
        "balancesheet",
        "cashflow",
        "analysis",
        "documents",
        "prosandcons",
        "sectors",
        "stock_prices",
        "financial_ratios",
        "market_cap",
        "peer_groups",
    ]


    primary_keys = {
        table: "id"
        for table in tables
    }



    required_columns = {

        "companies":["id","company_name"],
        "profitandloss":["id","company_id","year","sales"],
        "balancesheet":["id","company_id","year"],
        "cashflow":["id","company_id","year"],
        "analysis":["id","company_id"],
        "documents":["id","company_id"],
        "prosandcons":["id","company_id"],
        "sectors":["id","company_id"],
        "stock_prices":["id","company_id","date"],
        "financial_ratios":["id","company_id","year"],
        "market_cap":["id","company_id","year"],
        "peer_groups":["id","company_id"]

    }



    print("\n")
    print("="*60)
    print("DATA QUALITY VALIDATION REPORT")
    print("="*60)



    for table in tables:


        print("\nTable:", table)


        nulls = check_null_values(
            conn,
            table
        )


        duplicates = check_duplicates(
            conn,
            table
        )


        pk = check_primary_key(
            conn,
            table,
            primary_keys[table]
        )


        if table != "companies":

            fk = check_foreign_keys(
                conn,
                table
            )


        missing = check_required_columns(
            conn,
            table,
            required_columns[table]
        )


        datatype = check_data_types(
            conn,
            table
        )

        year_issue = check_year_format(
            conn,
            table
        )


        negative_issue = check_negative_values(
           conn,
           table
        )


        percentage_issue = check_percentage_range(
            conn,
            table
        )


        empty_issue = check_empty_table(
            conn,
            table
       )


        print(
            "Year Issues:",
            year_issue
        )

        print(
            "Negative Values:",
            negative_issue
        )

        print(
            "Percentage Issues:",
            percentage_issue
        )

        print(
            "Empty Table:",
            empty_issue
       ) 


        count = row_count(
            conn,
            table
        )


        print("Null Values:")
        print(nulls)

        print("Duplicate Rows:", duplicates)

        print("Primary Key Issues:", len(pk))

        print("Missing Columns:", len(missing))

        print("Data Type Issues:", len(datatype))

        print("Row Count:", count)



    REPORT_PATH.parent.mkdir(
        exist_ok=True
    )


    pd.DataFrame(
        VALIDATION_RESULTS
    ).to_csv(
        REPORT_PATH,
        index=False
    )


    print("\nValidation report saved:")
    print(REPORT_PATH)


    conn.close()



if __name__ == "__main__":

    validation_summary()