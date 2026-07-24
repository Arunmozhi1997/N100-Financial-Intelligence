"""
normaliser.py
Utility functions for cleaning and normalising data.
"""

import pandas as pd


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize column names.
    """
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )
    return df


def trim_text(df):
    """
    Remove leading/trailing whitespace from text columns
    while preserving missing values.
    """
    for col in df.select_dtypes(include="object"):
        df[col] = df[col].apply(
            lambda x: x.strip() if isinstance(x, str) else x
        )
    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate rows.
    """
    return df.drop_duplicates()


def normalize_year(value):
    """
    Normalize year values.
    Converts:
    2024.0 -> 2024
    "2024.0" -> 2024
    "FY2024" -> 2024
    "24" -> 2024
    """

    if pd.isna(value):
        return None


    # Handle numeric values
    if isinstance(value, (int, float)):

        year = int(float(value))

        if 1900 <= year <= 2100:
            return year

        return None



    value = str(value).strip()


    if value == "":
        return None



    # Remove decimal values like 2024.0

    if "." in value:

        try:
            value = str(int(float(value)))

        except ValueError:
            pass



    # Extract digits

    digits = "".join(
        ch for ch in value
        if ch.isdigit()
    )



    if len(digits) == 4:

        year = int(digits)

        if 1900 <= year <= 2100:
            return year



    if len(digits) == 2:

        year = int(digits)

        return (
            2000 + year
            if year < 50
            else 1900 + year
        )


    return None

def normalize_ticker(value):
    """
    Normalize stock ticker.
    """

    if value is None:
        return None

    if pd.isna(value):
        return None

    ticker = str(value).strip().upper()

    if ticker == "":
        return ""

    ticker = ticker.replace(" ", "")

    if ticker.endswith(".NS"):
        ticker = ticker[:-3]

    if ticker.endswith(".BO"):
        ticker = ticker[:-3]

    return ticker