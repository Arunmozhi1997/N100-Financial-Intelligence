from pathlib import Path

import pandas as pd
import sqlite3



# -----------------------------
# Project Paths
# -----------------------------
BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "db" / "nifty100.db"

OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "pros_cons_generated.csv"

def load_data():
    """Load required tables from SQLite database."""

    conn = sqlite3.connect(DB_PATH)

    companies = pd.read_sql("SELECT * FROM companies", conn)
    profit_loss = pd.read_sql("SELECT * FROM profitandloss", conn)
    balance_sheet = pd.read_sql("SELECT * FROM balancesheet", conn)
    cash_flow = pd.read_sql("SELECT * FROM cashflow", conn)
    financial_ratios = pd.read_sql("SELECT * FROM financial_ratios", conn)

    conn.close()

    return (
        companies,
        profit_loss,
        balance_sheet,
        cash_flow,
        financial_ratios,
    )

def pro_rule_1(financial_ratios):
    """
    ROE > 20% for at least 3 years
    """

    results = []

    grouped = financial_ratios.groupby("company_id")

    for company, df in grouped:

        df = df.sort_values("year")

        high_roe = (df["return_on_equity_pct"] > 20).sum()

        if high_roe >= 3:

            results.append(
                {
                    "company_id": company,
                    "type": "pro",
                    "rule_id": "PRO_01",
                    "text": (
                        "Consistently high return on equity above "
                        "20% demonstrates exceptional capital efficiency."
                    ),
                    "confidence_pct": 95,
                }
            )

    return results

def pro_rule_2(financial_ratios):
    """
    Positive Free Cash Flow for at least 5 years
    """

    results = []

    grouped = financial_ratios.groupby("company_id")

    for company, df in grouped:

        df = df.sort_values("year")

        positive_fcf = (df["free_cash_flow_cr"] > 0).sum()

        if positive_fcf >= 5:

            results.append(
                {
                    "company_id": company,
                    "type": "pro",
                    "rule_id": "PRO_02",
                    "text": (
                        "Strong free cash flow generation over 5 years "
                        "signals healthy business fundamentals."
                    ),
                    "confidence_pct": 90,
                }
            )

    return results

def pro_rule_3(financial_ratios):
    """
    Latest Debt-to-Equity = 0
    """

    results = []

    grouped = financial_ratios.groupby("company_id")

    for company, df in grouped:

        latest = df.sort_values("year").iloc[-1]

        if latest["debt_to_equity"] == 0:

            results.append(
                {
                    "company_id": company,
                    "type": "pro",
                    "rule_id": "PRO_03",
                    "text": (
                        "Debt-free balance sheet provides financial "
                        "flexibility and eliminates interest burden."
                    ),
                    "confidence_pct": 95,
                }
            )

    return results

def pro_rule_4(profit_loss):
    """
    Revenue CAGR > 15%
    """

    results = []

    grouped = profit_loss.groupby("company_id")

    for company, df in grouped:

        df = df.sort_values("year")

        if len(df) < 5:
            continue

        first = df.iloc[0]["sales"]
        last = df.iloc[-1]["sales"]

        if first <= 0:
            continue

        years = len(df) - 1

        cagr = ((last / first) ** (1 / years) - 1) * 100

        if cagr > 15:

            results.append(
                {
                    "company_id": company,
                    "type": "pro",
                    "rule_id": "PRO_04",
                    "text": (
                        "Revenue growing at above 15% CAGR over 5 years "
                        "reflects strong business momentum."
                    ),
                    "confidence_pct": 90,
                }
            )

    return results

def pro_rule_5(financial_ratios):
    """
    Latest Operating Profit Margin > 25%
    """

    results = []

    grouped = financial_ratios.groupby("company_id")

    for company, df in grouped:

        latest = df.sort_values("year").iloc[-1]

        if latest["operating_profit_margin_pct"] > 25:

            results.append(
                {
                    "company_id": company,
                    "type": "pro",
                    "rule_id": "PRO_05",
                    "text": (
                        "Operating profit margin above 25% indicates "
                        "strong pricing power and cost discipline."
                    ),
                    "confidence_pct": 90,
                }
            )

    return results

def pro_rule_6(profit_loss):
    """
    Net Profit CAGR > 20%
    """

    results = []

    grouped = profit_loss.groupby("company_id")

    for company, df in grouped:

        df = df.sort_values("year")

        if len(df) < 5:
            continue

        first = df.iloc[0]["net_profit"]
        last = df.iloc[-1]["net_profit"]

        if first <= 0:
            continue

        years = len(df) - 1

        cagr = ((last / first) ** (1 / years) - 1) * 100

        if cagr > 20:

            results.append(
                {
                    "company_id": company,
                    "type": "pro",
                    "rule_id": "PRO_06",
                    "text": (
                        "Net profit compounding at above 20% over 5 years "
                        "creates significant shareholder value."
                    ),
                    "confidence_pct": 92,
                }
            )

    return results

def pro_rule_7(financial_ratios):
    """
    Interest Coverage > 10 OR Debt Free
    """

    results = []

    grouped = financial_ratios.groupby("company_id")

    for company, df in grouped:

        latest = df.sort_values("year").iloc[-1]

        icr = latest["interest_coverage"]
        de = latest["debt_to_equity"]

        if icr > 10 or de == 0:

            results.append(
                {
                    "company_id": company,
                    "type": "pro",
                    "rule_id": "PRO_07",
                    "text": (
                        "Very high interest coverage ratio reflects "
                        "negligible financial stress from debt servicing."
                    ),
                    "confidence_pct": 90,
                }
            )

    return results

def pro_rule_8(financial_ratios):
    """
    Dividend payout supported by positive Free Cash Flow
    """

    results = []

    grouped = financial_ratios.groupby("company_id")

    for company, df in grouped:

        latest = df.sort_values("year").iloc[-1]

        if (
            latest["dividend_payout_ratio_pct"] > 20
            and latest["free_cash_flow_cr"] > 0
        ):

            results.append(
                {
                    "company_id": company,
                    "type": "pro",
                    "rule_id": "PRO_08",
                    "text": (
                        "Consistent dividend payout backed by positive free "
                        "cash flow reflects strong cash generation."
                    ),
                    "confidence_pct": 85,
                }
            )

    return results

def pro_rule_9(financial_ratios):
    """
    EPS CAGR > 15%
    """

    results = []

    grouped = financial_ratios.groupby("company_id")

    for company, df in grouped:

        df = df.sort_values("year")

        if len(df) < 5:
            continue

        first = df.iloc[0]["earnings_per_share"]
        last = df.iloc[-1]["earnings_per_share"]

        if first <= 0:
            continue

        years = len(df) - 1

        cagr = ((last / first) ** (1 / years) - 1) * 100

        if cagr > 15:

            results.append(
                {
                    "company_id": company,
                    "type": "pro",
                    "rule_id": "PRO_09",
                    "text": (
                        "Earnings per share growing above 15% CAGR "
                        "indicates strong earnings quality and compounding."
                    ),
                    "confidence_pct": 90,
                }
            )

    return results

def pro_rule_10(financial_ratios):
    """
    ROE improving for 3 consecutive years
    """

    results = []

    grouped = financial_ratios.groupby("company_id")

    for company, df in grouped:

        df = df.sort_values("year")

        if len(df) < 3:
            continue

        roe = df["return_on_equity_pct"].tail(3).tolist()

        if roe[0] < roe[1] < roe[2]:

            results.append(
                {
                    "company_id": company,
                    "type": "pro",
                    "rule_id": "PRO_10",
                    "text": (
                        "Return on equity improving for 3 consecutive years "
                        "shows strengthening business quality."
                    ),
                    "confidence_pct": 90,
                }
            )

    return results

def pro_rule_11(profit_loss):
    """
    PAT CAGR > Revenue CAGR (Operating Leverage)
    """

    results = []

    grouped = profit_loss.groupby("company_id")

    for company, df in grouped:

        df = df.sort_values("year")

        if len(df) < 5:
            continue

        sales_first = df.iloc[0]["sales"]
        sales_last = df.iloc[-1]["sales"]

        profit_first = df.iloc[0]["net_profit"]
        profit_last = df.iloc[-1]["net_profit"]

        if (
            sales_first <= 0
            or profit_first <= 0
        ):
            continue

        years = len(df) - 1

        sales_cagr = (
            ((sales_last / sales_first) ** (1 / years) - 1) * 100
        )

        profit_cagr = (
            ((profit_last / profit_first) ** (1 / years) - 1) * 100
        )

        if profit_cagr > sales_cagr:

            results.append(
                {
                    "company_id": company,
                    "type": "pro",
                    "rule_id": "PRO_11",
                    "text": (
                        "Revenue growing slower than profits shows improving "
                        "operating leverage and scale benefits."
                    ),
                    "confidence_pct": 90,
                }
            )

    return results

def pro_rule_12(balance_sheet):
    """
    Growing asset base with declining debt
    """

    results = []

    grouped = balance_sheet.groupby("company_id")

    for company, df in grouped:

        df = df.sort_values("year")

        if len(df) < 5:
            continue

        first_assets = df.iloc[0]["total_assets"]
        last_assets = df.iloc[-1]["total_assets"]

        first_debt = df.iloc[0]["borrowings"]
        last_debt = df.iloc[-1]["borrowings"]

        if (
            last_assets > first_assets
            and last_debt < first_debt
        ):

            results.append(
                {
                    "company_id": company,
                    "type": "pro",
                    "rule_id": "PRO_12",
                    "text": (
                        "Growing asset base funded by internal accruals "
                        "reflects self-sustaining growth."
                    ),
                    "confidence_pct": 90,
                }
            )

    return results

def con_rule_1(financial_ratios):
    """
    Debt-to-Equity > 2
    """

    results = []

    grouped = financial_ratios.groupby("company_id")

    for company, df in grouped:

        latest = df.sort_values("year").iloc[-1]

        if latest["debt_to_equity"] > 2:

            results.append(
                {
                    "company_id": company,
                    "type": "con",
                    "rule_id": "CON_01",
                    "text": (
                        f"Debt-to-equity ratio of "
                        f"{latest['debt_to_equity']:.2f} "
                        "is elevated and warrants monitoring."
                    ),
                    "confidence_pct": 95,
                }
            )

    return results


def con_rule_2(financial_ratios):
    """
    Free Cash Flow negative for 3 consecutive years
    """

    results = []

    grouped = financial_ratios.groupby("company_id")

    for company, df in grouped:

        df = df.sort_values("year")

        if len(df) < 3:
            continue

        last3 = df.tail(3)

        if (last3["free_cash_flow_cr"] < 0).all():

            results.append(
                {
                    "company_id": company,
                    "type": "con",
                    "rule_id": "CON_02",
                    "text": (
                        "Free cash flow negative for 3 consecutive years "
                        "raises concern about cash generation quality."
                    ),
                    "confidence_pct": 95,
                }
            )

    return results

def con_rule_3(financial_ratios):
    """
    Operating Profit Margin declining for 3 consecutive years
    """

    results = []

    grouped = financial_ratios.groupby("company_id")

    for company, df in grouped:

        df = df.sort_values("year")

        if len(df) < 3:
            continue

        opm = df["operating_profit_margin_pct"].tail(3).tolist()

        if opm[0] > opm[1] > opm[2]:

            results.append(
                {
                    "company_id": company,
                    "type": "con",
                    "rule_id": "CON_03",
                    "text": (
                        "Operating margins declining for 3 consecutive years "
                        "suggest pricing or cost pressure."
                    ),
                    "confidence_pct": 90,
                }
            )

    return results

def con_rule_4(profit_loss):
    """
    Net profit negative in latest year
    """

    results = []

    grouped = profit_loss.groupby("company_id")

    for company, df in grouped:

        latest = df.sort_values("year").iloc[-1]

        if latest["net_profit"] < 0:

            results.append(
                {
                    "company_id": company,
                    "type": "con",
                    "rule_id": "CON_04",
                    "text": (
                        "Company reported a net loss in the most recent financial year."
                    ),
                    "confidence_pct": 95,
                }
            )

    return results

def con_rule_5(profit_loss):
    """
    Revenue declining for 2 consecutive years
    """

    results = []

    grouped = profit_loss.groupby("company_id")

    for company, df in grouped:

        df = df.sort_values("year")

        if len(df) < 3:
            continue

        sales = df["sales"].tail(3).tolist()

        if sales[0] > sales[1] > sales[2]:

            results.append(
                {
                    "company_id": company,
                    "type": "con",
                    "rule_id": "CON_05",
                    "text": (
                        "Revenue contraction over 2 consecutive years "
                        "indicates demand weakness or market share loss."
                    ),
                    "confidence_pct": 90,
                }
            )

    return results

def con_rule_6(financial_ratios):
    """
    Interest Coverage Ratio < 1.5
    """

    results = []

    grouped = financial_ratios.groupby("company_id")

    for company, df in grouped:

        latest = df.sort_values("year").iloc[-1]

        if latest["interest_coverage"] < 1.5:

            results.append(
                {
                    "company_id": company,
                    "type": "con",
                    "rule_id": "CON_06",
                    "text": (
                        "Interest coverage ratio below 1.5x indicates the "
                        "company may struggle to meet debt obligations."
                    ),
                    "confidence_pct": 95,
                }
            )

    return results

def con_rule_7(financial_ratios):
    """
    Dividend Payout > 100%
    """

    results = []

    grouped = financial_ratios.groupby("company_id")

    for company, df in grouped:

        latest = df.sort_values("year").iloc[-1]

        if latest["dividend_payout_ratio_pct"] > 100:

            results.append(
                {
                    "company_id": company,
                    "type": "con",
                    "rule_id": "CON_07",
                    "text": (
                        "Dividend payout ratio above 100% suggests dividends "
                        "may be funded from reserves and could be unsustainable."
                    ),
                    "confidence_pct": 90,
                }
            )

    return results

def con_rule_8(financial_ratios):
    """
    Debt-to-Equity rising for 3 consecutive years
    """

    results = []

    grouped = financial_ratios.groupby("company_id")

    for company, df in grouped:

        df = df.sort_values("year")

        if len(df) < 3:
            continue

        debt = df["debt_to_equity"].tail(3).tolist()

        if debt[0] < debt[1] < debt[2]:

            results.append(
                {
                    "company_id": company,
                    "type": "con",
                    "rule_id": "CON_08",
                    "text": (
                        "Debt-to-equity ratio has increased for three "
                        "consecutive years, indicating rising financial leverage."
                    ),
                    "confidence_pct": 90,
                }
            )

    return results

def con_rule_9(financial_ratios):
    """
    EPS declining for 3 consecutive years
    """

    results = []

    grouped = financial_ratios.groupby("company_id")

    for company, df in grouped:

        df = df.sort_values("year")

        if len(df) < 3:
            continue

        eps = df["earnings_per_share"].tail(3).tolist()

        if eps[0] > eps[1] > eps[2]:

            results.append(
                {
                    "company_id": company,
                    "type": "con",
                    "rule_id": "CON_09",
                    "text": (
                        "Earnings per share have declined for three consecutive years, "
                        "reflecting deteriorating profitability."
                    ),
                    "confidence_pct": 90,
                }
            )

    return results

def con_rule_10(companies):
    """
    ROCE < 10%
    """

    results = []

    for _, row in companies.iterrows():

        if row["roce_percentage"] < 10:

            results.append(
                {
                    "company_id": row["id"],
                    "type": "con",
                    "rule_id": "CON_10",
                    "text": (
                        "Return on capital employed below 10% suggests the business "
                        "is not generating sufficient returns on invested capital."
                    ),
                    "confidence_pct": 90,
                }
            )

    return results

def con_rule_12(profit_loss):
    """
    Revenue CAGR < 5%
    """

    results = []

    grouped = profit_loss.groupby("company_id")

    for company, df in grouped:

        df = df.sort_values("year")

        if len(df) < 5:
            continue

        first = df.iloc[0]["sales"]
        last = df.iloc[-1]["sales"]

        years = len(df) - 1

        if first <= 0:
            continue

        cagr = ((last / first) ** (1 / years) - 1) * 100

        if cagr < 5:

            results.append(
                {
                    "company_id": company,
                    "type": "con",
                    "rule_id": "CON_12",
                    "text": (
                        "Revenue growing below 5% CAGR over the last five years "
                        "suggests limited business momentum."
                    ),
                    "confidence_pct": 85,
                }
            )

    return results


def main():

    (
        companies,
        profit_loss,
        balance_sheet,
        cash_flow,
        financial_ratios,
    ) = load_data()

    rule1 = pro_rule_1(financial_ratios)
    rule2 = pro_rule_2(financial_ratios)
    rule3 = pro_rule_3(financial_ratios)
    rule4 = pro_rule_4(profit_loss)
    rule5 = pro_rule_5(financial_ratios)
    rule6 = pro_rule_6(profit_loss)
    rule7 = pro_rule_7(financial_ratios)
    rule8 = pro_rule_8(financial_ratios)
    rule9 = pro_rule_9(financial_ratios)
    rule10 = pro_rule_10(financial_ratios)
    rule11 = pro_rule_11(profit_loss)
    rule12 = pro_rule_12(balance_sheet)

    con1 = con_rule_1(financial_ratios)
    con2 = con_rule_2(financial_ratios)
    con3 = con_rule_3(financial_ratios)
    con4 = con_rule_4(profit_loss)
    con5 = con_rule_5(profit_loss)
    con6 = con_rule_6(financial_ratios)
    con7 = con_rule_7(financial_ratios)
    con8 = con_rule_8(financial_ratios)
    con9 = con_rule_9(financial_ratios)
    con10 = con_rule_10(companies)
    con12 = con_rule_12(profit_loss)

    pros = []

    pros.extend(rule1)
    pros.extend(rule2)
    pros.extend(rule3)
    pros.extend(rule4)
    pros.extend(rule5)
    pros.extend(rule6)
    pros.extend(rule7)
    pros.extend(rule8)
    pros.extend(rule9)
    pros.extend(rule10)
    pros.extend(rule11)
    pros.extend(rule12)
    

    cons = []

    cons.extend(con1)
    cons.extend(con2)
    cons.extend(con3)
    cons.extend(con4)
    cons.extend(con5)
    cons.extend(con6)
    cons.extend(con7)
    cons.extend(con8)
    cons.extend(con9)
    cons.extend(con10)
    cons.extend(con12)

    result = pd.DataFrame(pros + cons)

    result.to_csv(OUTPUT_FILE, index=False)

    print(result.head())

    print()

    print(f"Rule 1 Companies : {len(rule1)}")
    print(f"Rule 2 Companies : {len(rule2)}")
    print(f"Rule 3 Companies : {len(rule3)}")
    print(f"Rule 4 Companies : {len(rule4)}")
    print(f"Rule 5 Companies : {len(rule5)}")
    print(f"Rule 6 Companies : {len(rule6)}")
    print(f"Rule 7 Companies : {len(rule7)}")
    print(f"Rule 8 Companies : {len(rule8)}")
    print(f"Rule 9 Companies : {len(rule9)}")
    print(f"Rule 10 Companies : {len(rule10)}")
    print(f"Rule 11 Companies : {len(rule11)}")
    print(f"Rule 12 Companies : {len(rule12)}")

    print(f"CON 1 Companies : {len(con1)}")
    print(f"CON 2 Companies : {len(con2)}")
    print(f"CON 3 Companies : {len(con3)}")
    print(f"CON 4 Companies : {len(con4)}")
    print(f"CON 5 Companies : {len(con5)}")
    print(f"CON 6 Companies : {len(con6)}")
    print(f"CON 7 Companies : {len(con7)}")
    print(f"CON 8 Companies : {len(con8)}")
    print(f"CON 9 Companies : {len(con9)}")
    print(f"CON 10 Companies : {len(con10)}")
    print(f"CON 12 Companies : {len(con12)}")

    print(f"Total Pro Records: {len(result)}")


if __name__ == "__main__":
    main()