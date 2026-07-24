"""
config.py
Project configuration file
"""

from pathlib import Path

# Project Root
BASE_DIR = Path(__file__).resolve().parents[2]

# Data folders
DATA_DIR = BASE_DIR / "data"
RAW_DATA = DATA_DIR / "raw"
PROCESSED_DATA = DATA_DIR / "processed"

# Database
DB_DIR = BASE_DIR / "db"
DB_PATH = DB_DIR / "nifty100.db"

# Output
OUTPUT_DIR = BASE_DIR / "output"

# Logs
LOG_DIR = BASE_DIR / "logs"

# Create folders if they don't exist
for folder in (
    RAW_DATA,
    PROCESSED_DATA,
    DB_DIR,
    OUTPUT_DIR,
    LOG_DIR,
):
    folder.mkdir(parents=True, exist_ok=True)
