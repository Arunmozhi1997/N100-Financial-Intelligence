import sqlite3
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "db" / "nifty100.db"

conn = sqlite3.connect(DB_PATH)

# Pick 5 random companies
query = """
SELECT id, company_name
FROM companies
ORDER BY RANDOM()
LIMIT 5
"""

companies = pd.read_sql_query(query, conn)

print("\nRandom Companies")
print("=" * 50)
print(companies)

print("\n")
print("=" * 60)
print("YEAR COVERAGE")
print("=" * 60)

for company_id in companies["id"]:

    print(f"\nCompany: {company_id}")

    query = f"""
    SELECT year
    FROM profitandloss
    WHERE company_id = '{company_id}'
    ORDER BY year
    """

    years = pd.read_sql_query(query, conn)

    print(years)

print("\n")
print("=" * 60)
print("COMPANIES WITH LESS THAN 5 YEARS OF DATA")
print("=" * 60)

query = """
SELECT
    company_id,
    COUNT(year) AS total_years
FROM profitandloss
WHERE year IS NOT NULL
GROUP BY company_id
HAVING COUNT(year) < 5
ORDER BY total_years;
"""

result = pd.read_sql_query(query, conn)

print(result)

conn.close()
