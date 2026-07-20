"""
loader.py

Reads all Excel files and loads them into SQLite.
"""

from pathlib import Path
import sqlite3
import pandas as pd
from datetime import datetime

from src.etl.config import (
    RAW_DATA,
    DB_PATH,
    OUTPUT_DIR,
)

from src.etl.normaliser import (
    normalize_columns,
    trim_text,
    remove_duplicates,
    normalize_year,
    normalize_ticker,
)

# Files whose real headers start on the second row
TITLE_ROW_FILES = {
    "companies.xlsx",
    "profitandloss.xlsx",
    "balancesheet.xlsx",
    "cashflow.xlsx",
    "analysis.xlsx",
    "documents.xlsx",
    "prosandcons.xlsx",
}

# Mapping: Excel file -> SQLite table
TABLE_MAPPING = {
    "companies.xlsx": "companies",
    "profitandloss.xlsx": "profitandloss",
    "balancesheet.xlsx": "balancesheet",
    "cashflow.xlsx": "cashflow",
    "analysis.xlsx": "analysis",
    "documents.xlsx": "documents",
    "prosandcons.xlsx": "prosandcons",
    "sectors.xlsx": "sectors",
    "stock_prices.xlsx": "stock_prices",
    "financial_ratios.xlsx": "financial_ratios",
    "market_cap.xlsx": "market_cap",
    "peer_groups.xlsx": "peer_groups",
}

def read_excel(file_path: Path) -> pd.DataFrame:
    """
    Read an Excel file using the correct header row.
    """

    if file_path.name in TITLE_ROW_FILES:
        df = pd.read_excel(file_path, header=1)
    else:
        df = pd.read_excel(file_path)

    df = normalize_columns(df)
    df = trim_text(df)
    df = remove_duplicates(df)

    # Normalize year column if present
    if "year" in df.columns:
        df["year"] = df["year"].apply(normalize_year)

    # Normalize company_id if present
    if "company_id" in df.columns:
        df["company_id"] = df["company_id"].apply(normalize_ticker)

    return df


def get_connection():
    """
    Create SQLite connection.
    """

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")

    return conn

def clear_tables(conn):
    """
    Delete all old records.
    """

    conn.execute("PRAGMA foreign_keys = OFF")

    tables = [
        "cashflow",
        "balancesheet",
        "profitandloss",
        "analysis",
        "documents",
        "prosandcons",
        "stock_prices",
        "financial_ratios",
        "market_cap",
        "peer_groups",
        "companies",
        "sectors",
    ]

    for table in tables:
        try:
            conn.execute(f"DELETE FROM {table}")
            print(f"Cleared {table}")
        except Exception as e:
            print(f"Skipped {table}: {e}")

    conn.commit()

    conn.execute("PRAGMA foreign_keys = ON")



def load_table(conn, table_name, df):
    """
    Load one DataFrame into SQLite.
    """

    # Add missing companies
    if table_name == "companies":

        missing = [
            "AGTL",
            "ULTRACEMCO",
            "UNIONBANK",
            "UNITDSPR",
            "VBL",
            "VEDL",
            "WIPRO",
            "ZOMATO",
            "ZYDUSLIFE",
        ]

        existing_ids = set(
            df["id"].astype(str).str.strip()
        )

        for cid in missing:

            if cid not in existing_ids:

                row = {
                    col: None
                    for col in df.columns
                }

                row["id"] = cid
                row["company_name"] = cid

                df = pd.concat(
                    [
                        df,
                        pd.DataFrame([row])
                    ],
                    ignore_index=True
                )

                existing_ids.add(cid)

        # Remove duplicate company IDs
        df["id"] = df["id"].astype(str).str.strip()
        df = df.drop_duplicates(
            subset=["id"],
            keep="first"
        )

        # Print duplicates if any still exist
        duplicates = df[
            df.duplicated(
                subset=["id"],
                keep=False
            )
        ]

        if not duplicates.empty:
            print("\nDuplicate Company IDs Found:")
            print(
                duplicates[
                    ["id", "company_name"]
                ]
            )

    # Insert into SQLite
    df.to_sql(
        table_name,
        conn,
        if_exists="append",
        index=False
    )

    conn.commit()



def main():

    conn = get_connection()

    total_rows = 0

    audit_log = []


    print("\nClearing old database tables...")
    clear_tables(conn)


    total_rows = 0


    for excel_file, table_name in TABLE_MAPPING.items():

        file_path = RAW_DATA / excel_file


        print(
            f"\nLoading {excel_file}"
        )


        df = read_excel(file_path)



        # Debug cashflow foreign keys
        if table_name == "cashflow":

            companies = pd.read_sql_query(
                "SELECT id FROM companies",
                conn
            )


            company_ids = set(
                companies["id"]
                .astype(str)
                .str.strip()
            )


            cash_ids = set(
                df["company_id"]
                .astype(str)
                .str.strip()
            )


            missing = sorted(
                cash_ids - company_ids
            )


            print(
                "\nMissing Company IDs in cashflow:"
            )

            print(missing)


            print(
                "\nTotal Missing:",
                len(missing)
            )



        load_table(
            conn,
            table_name,
            df
        )


        print(
            f"Loaded {len(df)} rows into {table_name}"
        )


        total_rows += len(df)

        audit_log.append(
           {
             "table_name": table_name,
             "rows_loaded": len(df),
             "status": "SUCCESS",
             "loaded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
           }
        )

    # Save load audit report
    audit_df = pd.DataFrame(audit_log)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    audit_file = OUTPUT_DIR / "load_audit.csv"


    audit_df.to_csv(
       audit_file,
       index=False
       )

    print("\nLoad audit saved:")
    print(audit_file)    
        




    conn.close()


    print("\n" + "=" * 60)
    print("ETL Completed Successfully")
    print(f"Total Rows Loaded : {total_rows}")
    print("=" * 60)



if __name__ == "__main__":
    main()