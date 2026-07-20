import pandas as pd

from src.etl.normaliser import (
    normalize_columns,
    trim_text,
    remove_duplicates,
    normalize_year,
    normalize_ticker,
)


# ======================================================
# normalize_columns (5 Tests)
# ======================================================

def test_normalize_columns_spaces():
    df = pd.DataFrame(columns=["Company Name"])
    df = normalize_columns(df)
    assert "company_name" in df.columns


def test_normalize_columns_dash():
    df = pd.DataFrame(columns=["Book-Value"])
    df = normalize_columns(df)
    assert "book_value" in df.columns


def test_normalize_columns_strip():
    df = pd.DataFrame(columns=["  Sales  "])
    df = normalize_columns(df)
    assert "sales" in df.columns


def test_normalize_columns_lower():
    df = pd.DataFrame(columns=["EPS"])
    df = normalize_columns(df)
    assert "eps" in df.columns


def test_normalize_columns_multiple():
    df = pd.DataFrame(columns=["Company Name", "Book-Value"])
    df = normalize_columns(df)
    assert list(df.columns) == ["company_name", "book_value"]


# ======================================================
# trim_text (5 Tests)
# ======================================================

def test_trim_text_spaces():
    df = pd.DataFrame({"name": ["  TCS  "]})
    df = trim_text(df)
    assert df.loc[0, "name"] == "TCS"


def test_trim_text_none():
    df = pd.DataFrame({"name": [None]})
    df = trim_text(df)
    assert df.loc[0, "name"] is None


def test_trim_text_number():
    df = pd.DataFrame({"value": [100]})
    df = trim_text(df)
    assert df.loc[0, "value"] == 100


def test_trim_text_multiple():
    df = pd.DataFrame({"name": [" A ", " B "]})
    df = trim_text(df)
    assert df["name"].tolist() == ["A", "B"]


def test_trim_text_empty():
    df = pd.DataFrame({"name": [""]})
    df = trim_text(df)
    assert df.loc[0, "name"] == ""


# ======================================================
# remove_duplicates (5 Tests)
# ======================================================

def test_remove_duplicates_one():
    df = pd.DataFrame({"A": [1, 1]})
    df = remove_duplicates(df)
    assert len(df) == 1


def test_remove_duplicates_none():
    df = pd.DataFrame({"A": [1, 2]})
    df = remove_duplicates(df)
    assert len(df) == 2


def test_remove_duplicates_three():
    df = pd.DataFrame({"A": [1, 1, 1]})
    df = remove_duplicates(df)
    assert len(df) == 1


def test_remove_duplicates_text():
    df = pd.DataFrame({"A": ["TCS", "TCS"]})
    df = remove_duplicates(df)
    assert len(df) == 1


def test_remove_duplicates_multi_column():
    df = pd.DataFrame({
        "A": [1, 1],
        "B": [2, 2]
    })
    df = remove_duplicates(df)
    assert len(df) == 1


# ======================================================
# normalize_year (10 Tests)
# ======================================================

def test_year_none():
    assert normalize_year(None) is None


def test_year_nan():
    assert normalize_year(float("nan")) is None


def test_year_2024():
    assert normalize_year("2024") == 2024


def test_year_dec2012():
    assert normalize_year("Dec 2012") == 2012


def test_year_mar2014():
    assert normalize_year("Mar 2014") == 2014


def test_year_mar15():
    assert normalize_year("Mar-15") == 2015


def test_year_99():
    assert normalize_year("99") == 1999


def test_year_spaces():
    assert normalize_year(" 2023 ") == 2023


def test_year_invalid():
    assert normalize_year("ABC") is None


def test_year_empty():
    assert normalize_year("") is None


# ======================================================
# normalize_ticker (10 Tests)
# ======================================================

def test_ticker_lower():
    assert normalize_ticker("tcs") == "TCS"


def test_ticker_upper():
    assert normalize_ticker("TCS") == "TCS"


def test_ticker_spaces():
    assert normalize_ticker(" tcs ") == "TCS"


def test_ticker_none():
    assert normalize_ticker(None) is None


def test_ticker_empty():
    assert normalize_ticker("") == ""


def test_ticker_number():
    assert normalize_ticker(123) == "123"


def test_ticker_infy():
    assert normalize_ticker("infy") == "INFY"


def test_ticker_reliance():
    assert normalize_ticker(" reliance ") == "RELIANCE"


def test_ticker_hdfc():
    assert normalize_ticker("hdfc") == "HDFC"


def test_ticker_mixed():
    assert normalize_ticker("TcS") == "TCS"