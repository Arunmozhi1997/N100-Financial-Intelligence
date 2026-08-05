import sqlite3
import pandas as pd

DB_PATH = "db/nifty100.db"

def free_cash_flow(operating_activity, investing_activity):
    """
    Calculate Free Cash Flow (FCF).

    Formula:
        FCF = Operating Activity + Investing Activity

    Note:
        Investing activity is usually negative.
        A negative FCF is allowed.
    """

    return operating_activity + investing_activity


def cfo_quality_score(cfo, pat):
    """
    Calculate CFO Quality Score.

    Formula:
        CFO / PAT

    Returns:
        tuple -> (ratio, quality_label)

        High Quality : ratio > 1.0
        Moderate     : 0.5 <= ratio <= 1.0
        Accrual Risk : ratio < 0.5
        None         : if PAT is zero
    """

    if pat == 0:
        return None, None

    ratio = cfo / pat

    if ratio > 1.0:
        label = "High Quality"
    elif ratio >= 0.5:
        label = "Moderate"
    else:
        label = "Accrual Risk"

    return ratio, label


def capex_intensity(investing_activity, sales):
    """
    Calculate CapEx Intensity.

    Formula:
        abs(Investing Activity) / Sales * 100

    Returns:
        tuple -> (capex_percentage, category)

        Asset Light       : < 3%
        Moderate          : 3% to 8%
        Capital Intensive : > 8%
        None              : if sales is zero
    """

    if sales == 0:
        return None, None

    percentage = (abs(investing_activity) / sales) * 100

    if percentage < 3:
        category = "Asset Light"
    elif percentage <= 8:
        category = "Moderate"
    else:
        category = "Capital Intensive"

    return percentage, category


def fcf_conversion_rate(free_cash_flow, operating_profit):
    """
    Calculate Free Cash Flow Conversion Rate.

    Formula:
        (Free Cash Flow / Operating Profit) * 100

    Returns:
        float : Conversion percentage
        None  : If operating_profit is zero
    """

    if operating_profit == 0:
        return None

    return (free_cash_flow / operating_profit) * 100


def capital_allocation_pattern(
    operating_activity,
    investing_activity,
    financing_activity,
    cfo_pat_ratio=None,
):
    """
    Classify capital allocation pattern based on the signs of
    CFO (Operating), CFI (Investing), and CFF (Financing).

    Parameters
    ----------
    operating_activity : float
    investing_activity : float
    financing_activity : float
    cfo_pat_ratio : float, optional
        CFO / PAT ratio used to distinguish Shareholder Returns
        from Reinvestor.

    Returns
    -------
    tuple
        (cfo_sign, cfi_sign, cff_sign, pattern_label)
    """

    cfo_sign = "+" if operating_activity >= 0 else "-"
    cfi_sign = "+" if investing_activity >= 0 else "-"
    cff_sign = "+" if financing_activity >= 0 else "-"

    pattern = "Unknown"

    if (cfo_sign, cfi_sign, cff_sign) == ("+", "-", "-"):
        if cfo_pat_ratio is not None and cfo_pat_ratio > 1.0:
            pattern = "Shareholder Returns"
        else:
            pattern = "Reinvestor"

    elif (cfo_sign, cfi_sign, cff_sign) == ("+", "+", "-"):
        pattern = "Liquidating Assets"

    elif (cfo_sign, cfi_sign, cff_sign) == ("-", "+", "+"):
        pattern = "Distress Signal"

    elif (cfo_sign, cfi_sign, cff_sign) == ("-", "-", "+"):
        pattern = "Growth Funded by Debt"

    elif (cfo_sign, cfi_sign, cff_sign) == ("+", "+", "+"):
        pattern = "Cash Accumulator"

    elif (cfo_sign, cfi_sign, cff_sign) == ("-", "-", "-"):
        pattern = "Pre-Revenue"

    elif (cfo_sign, cfi_sign, cff_sign) == ("+", "-", "+"):
        pattern = "Mixed"

    return (
        cfo_sign,
        cfi_sign,
        cff_sign,
        pattern,
    )

def distress_flag(
    operating_activity,
    financing_activity,
):
    """
    Distress Signal:
    CFO < 0 AND Financing Cash Flow > 0
    """

    if (
        operating_activity < 0
        and financing_activity > 0
    ):
        return "Yes"

    return "No"

def deleveraging_flag(
    operating_activity,
    financing_activity,
):

    if (
        operating_activity > 0
        and financing_activity < 0
    ):
        return "Yes"

    return "No"


def cashflow_score(
    free_cash_flow,
    cfo_quality_score,
    fcf_conversion_pct,
    capex_label,
    capital_allocation_label,
):

    score = 0

    # Positive Free Cash Flow
    if free_cash_flow > 0:
        score += 20

    # Good CFO Quality
    if (
        cfo_quality_score is not None
        and cfo_quality_score > 1
    ):
        score += 20

    # Good FCF Conversion
    if (
        fcf_conversion_pct is not None
        and fcf_conversion_pct > 50
    ):
        score += 20

    # Efficient CapEx
    if capex_label in [
        "Asset Light",
        "Moderate",
    ]:
        score += 20

    # Healthy Capital Allocation
    if capital_allocation_label in [
        "Shareholder Returns",
        "Reinvestor",
    ]:
        score += 20

    return score


def cashflow_grade(score):

    if score >= 90:
        return "A+"

    elif score >= 80:
        return "A"

    elif score >= 70:
        return "B"

    elif score >= 60:
        return "C"

    else:
        return "D"



def load_database():

    conn = sqlite3.connect(DB_PATH)

    companies = pd.read_sql(
        "SELECT * FROM companies",
        conn,
    )

    profit_loss = pd.read_sql(
        "SELECT * FROM profitandloss",
        conn,
    )

    cashflow = pd.read_sql(
        "SELECT * FROM cashflow",
        conn,
    )

    sectors = pd.read_sql(
        "SELECT * FROM sectors",
        conn,
    )

    conn.close()

    return (
        companies,
        profit_loss,
        cashflow,
        sectors,
    )

def calculate_fcf_cagr(df):

    rows = []

    for company, group in df.groupby("company_id"):

        group = group.sort_values("year")

        if len(group) < 5:
            continue

        last5 = group.tail(5)

        first = last5.iloc[0]["free_cash_flow"]
        last = last5.iloc[-1]["free_cash_flow"]

        if first <= 0 or last <= 0:
            continue

        cagr = ((last / first) ** (1 / 4) - 1) * 100

        rows.append(
            {
                "company_id": company,
                "fcf_cagr_5yr": round(cagr, 2),
            }
        )

    return pd.DataFrame(rows)


def main():

    companies, profit_loss, cashflow, sectors = load_database()

    print("Database Loaded Successfully\n")

    print("Companies :", len(companies))
    print("Profit & Loss :", len(profit_loss))
    print("Cash Flow :", len(cashflow))

    # ---------------------------------------------------
    # Clean Year
    # ---------------------------------------------------

    profit_loss["year"] = pd.to_numeric(
        profit_loss["year"],
        errors="coerce",
    )

    cashflow["year"] = pd.to_numeric(
        cashflow["year"],
        errors="coerce",
    )

    profit_loss = profit_loss.dropna(subset=["year"])
    cashflow = cashflow.dropna(subset=["year"])

    profit_loss["year"] = profit_loss["year"].astype(int)
    cashflow["year"] = cashflow["year"].astype(int)

    # ---------------------------------------------------
    # Clean Company IDs
    # ---------------------------------------------------

    profit_loss["company_id"] = (
        profit_loss["company_id"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    cashflow["company_id"] = (
        cashflow["company_id"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    # ---------------------------------------------------
    # Remove duplicate company-year rows
    # ---------------------------------------------------

    cashflow = (
        cashflow
        .sort_values("id")
        .drop_duplicates(
            subset=["company_id", "year"],
            keep="first",
        )
    )


# ----------------------------
# Clean Sectors
# ----------------------------

    sectors["company_id"] = (
       sectors["company_id"]
       .astype(str)
        .str.strip()
        .str.upper()
    )

    sectors = sectors.drop_duplicates(
        subset=["company_id"],

    )

    # ---------------------------------------------------
    # Merge
    # ---------------------------------------------------

    df = profit_loss.merge(
        cashflow,
        on=["company_id", "year"],
        how="inner",
    )

    df = df.merge(
    sectors[
        [
            "company_id",
            "broad_sector",
        ]
    ],
    on="company_id",
    how="left",
    )

    df.rename(
    columns={
        "broad_sector": "sector"
    },
    inplace=True,
    )

    print()
    print("Merged Rows :", len(df))
    print()

    # ---------------------------------------------------
    # Free Cash Flow
    # ---------------------------------------------------

    df["free_cash_flow"] = df.apply(
        lambda x: free_cash_flow(
            x["operating_activity"],
            x["investing_activity"],
        ),
        axis=1,
    )

# ---------------------------------------------------
# FCF CAGR (5 Years)
# ---------------------------------------------------

    fcf_cagr = calculate_fcf_cagr(df)

    df = df.merge(
       fcf_cagr,
       on="company_id",
       how="left",
    )

    # ---------------------------------------------------
    # CFO Quality
    # ---------------------------------------------------

    quality = df.apply(
        lambda x: cfo_quality_score(
            x["operating_activity"],
            x["net_profit"],
        ),
        axis=1,
    )

    df["cfo_quality_score"] = quality.apply(lambda x: x[0])
    df["cfo_quality_label"] = quality.apply(lambda x: x[1])

    # ---------------------------------------------------
    # CapEx Intensity
    # ---------------------------------------------------

    capex = df.apply(
        lambda x: capex_intensity(
            x["investing_activity"],
            x["sales"],
        ),
        axis=1,
    )

    df["capex_intensity_pct"] = capex.apply(lambda x: x[0])
    df["capex_label"] = capex.apply(lambda x: x[1])

    # ---------------------------------------------------
    # FCF Conversion
    # ---------------------------------------------------

    df["fcf_conversion_pct"] = df.apply(
        lambda x: fcf_conversion_rate(
            x["free_cash_flow"],
            x["operating_profit"],
        ),
        axis=1,
    )

    # ---------------------------------------------------
    # Capital Allocation Pattern
    # ---------------------------------------------------

    allocation = df.apply(
        lambda x: capital_allocation_pattern(
            x["operating_activity"],
            x["investing_activity"],
            x["financing_activity"],
            x["cfo_quality_score"],
        ),
        axis=1,
    )

    df["cfo_sign"] = allocation.apply(lambda x: x[0])
    df["cfi_sign"] = allocation.apply(lambda x: x[1])
    df["cff_sign"] = allocation.apply(lambda x: x[2])
    df["capital_allocation_label"] = allocation.apply(lambda x: x[3])

# ---------------------------------------------------
# Distress Flag
# ---------------------------------------------------

    df["distress_flag"] = df.apply(
       lambda x: distress_flag(
          x["operating_activity"],
          x["financing_activity"],
        ),
        axis=1,
    )

# ---------------------------------------------------
# Deleveraging Flag
# ---------------------------------------------------

    df["deleveraging_flag"] = df.apply(
        lambda x: deleveraging_flag(
            x["operating_activity"],
            x["financing_activity"],
        ),
        axis=1,
    )

# ---------------------------------------------------
# Cash Flow Score
# ---------------------------------------------------

    df["cashflow_score"] = df.apply(
        lambda x: cashflow_score(
           x["free_cash_flow"],
           x["cfo_quality_score"],
           x["fcf_conversion_pct"],
           x["capex_label"],
           x["capital_allocation_label"],
        ),
        axis=1,
    )

# ---------------------------------------------------
# Cash Flow Grade
# ---------------------------------------------------

    df["cashflow_grade"] = df["cashflow_score"].apply(
        cashflow_grade
    )


    # ---------------------------------------------------
    # Preview
    # ---------------------------------------------------

    print(
        df[
            [
                "company_id",
                "sector",
                "year",
                "free_cash_flow",
                "cfo_quality_score",
                "cfo_quality_label",
                "capex_intensity_pct",
                "capex_label",
                "fcf_cagr_5yr",
                "fcf_conversion_pct",
                "capital_allocation_label",
                "distress_flag",
                "deleveraging_flag",
                "cashflow_score",
                "cashflow_grade",
            ]
        ].head(10)
    )

    # ---------------------------------------------------
    # Save
    # ---------------------------------------------------
    alerts = df[df["distress_flag"] == "Yes"][
    [
        "company_id",
        "sector",
        "year",
        "operating_activity",
        "financing_activity",
        "net_profit",
    ]
]

    alerts.to_csv(
       "output/distress_alerts.csv",
       index=False,
    )

    print("Distress Alerts :", len(alerts))



    df.to_excel(
        "output/cashflow_intelligence.xlsx",
        index=False,
    )

    print()
    print("Saved - output/cashflow_intelligence.xlsx")

    conn = sqlite3.connect(DB_PATH)

    try:
        df.to_sql(
           "cashflow_intelligence",
            conn,
            if_exists="replace",
            index=False,
        )
    finally:
       conn.close()


if __name__ == "__main__":
    main()