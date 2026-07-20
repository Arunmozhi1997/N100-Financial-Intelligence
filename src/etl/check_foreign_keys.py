import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "db" / "nifty100.db"

conn = sqlite3.connect(DB_PATH)

result = conn.execute(
    "PRAGMA foreign_key_check;"
).fetchall()

print("\nForeign Key Check")
print("=" * 50)

if len(result) == 0:
    print("PASS - No foreign key violations found.")
else:
    print("FAIL - Foreign key violations found:")
    for row in result:
        print(row)

conn.close()