import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "db" / "nifty100.db"


conn = sqlite3.connect(DB_PATH)


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


for table in tables:

    print("\n----------------")
    print("Table:", table)

    columns = conn.execute(
        f"PRAGMA table_info({table})"
    ).fetchall()

    for col in columns:
        print(col[1])


conn.close()
