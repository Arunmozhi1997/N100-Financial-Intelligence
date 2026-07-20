"""
create_database.py

Creates the SQLite database using db/schema.sql
"""

import sqlite3
from pathlib import Path

from src.etl.config import DB_PATH, BASE_DIR


def create_database():
    """Create SQLite database and all tables."""

    schema_path = BASE_DIR / "db" / "schema.sql"

    if not schema_path.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")

    conn = sqlite3.connect(DB_PATH)

    # Enable Foreign Keys
    conn.execute("PRAGMA foreign_keys = ON;")

    with open(schema_path, "r", encoding="utf-8") as f:
        sql_script = f.read()

    conn.executescript(sql_script)

    conn.commit()
    conn.close()

    print("=" * 60)
    print("✅ Database Created Successfully")
    print(f"Database : {DB_PATH}")
    print("=" * 60)


if __name__ == "__main__":
    create_database()