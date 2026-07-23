def net_profit_margin(net_profit, sales):
    """
    Calculate Net Profit Margin (%)

    Formula:
        Net Profit Margin = (Net Profit / Sales) * 100

    Returns:
        float: Net Profit Margin percentage
        None: If sales is zero
    """

    if sales == 0:
        return None

    return (net_profit / sales) * 100

def operating_profit_margin(operating_profit, sales):
    """
    Calculate Operating Profit Margin (%)

    Formula:
        Operating Profit Margin = (Operating Profit / Sales) * 100

    Returns:
        float: Operating Profit Margin percentage
        None: If sales is zero
    """

    if sales == 0:
        return None

    return (operating_profit / sales) * 100

def return_on_equity(net_profit, equity_capital, reserves):
    """
    Calculate Return on Equity (ROE) (%)

    Formula:
        ROE = (Net Profit / (Equity Capital + Reserves)) * 100

    Returns:
        float: ROE percentage
        None: If Equity + Reserves <= 0
    """

    total_equity = equity_capital + reserves

    if total_equity <= 0:
        return None

    return (net_profit / total_equity) * 100

def return_on_capital_employed(
    ebit,
    equity_capital,
    reserves,
    borrowings,
):
    """
    Calculate Return on Capital Employed (ROCE) (%)

    Formula:
        ROCE = (EBIT / (Equity Capital + Reserves + Borrowings)) * 100

    Returns:
        float: ROCE percentage
        None: If capital employed <= 0
    """

    capital_employed = equity_capital + reserves + borrowings

    if capital_employed <= 0:
        return None

    return (ebit / capital_employed) * 100


def return_on_assets(net_profit, total_assets):
    """
    Calculate Return on Assets (ROA) (%)

    Formula:
        ROA = (Net Profit / Total Assets) * 100

    Returns:
        float: ROA percentage
        None: If total_assets is zero
    """

    if total_assets == 0:
        return None

    return (net_profit / total_assets) * 100


def check_opm_difference(calculated_opm, source_opm, tolerance=1.0):
    """
    Compare calculated OPM with source OPM.

    Parameters:
        calculated_opm (float): OPM calculated by the ratio engine.
        source_opm (float): OPM from the source dataset.
        tolerance (float): Allowed percentage difference.

    Returns:
        bool:
            True  -> Difference is greater than tolerance.
            False -> Difference is within tolerance.
    """

    if calculated_opm is None or source_opm is None:
        return False

    return abs(calculated_opm - source_opm) > tolerance


def debt_to_equity(borrowings, equity_capital, reserves):
    """
    Calculate Debt-to-Equity Ratio.

    Formula:
        Debt-to-Equity = Borrowings / (Equity Capital + Reserves)

    Returns:
        float: Debt-to-Equity Ratio
        0: If borrowings are zero
        None: If equity is zero or negative
    """

    if borrowings == 0:
        return 0

    total_equity = equity_capital + reserves

    if total_equity <= 0:
        return None

    return borrowings / total_equity


def high_leverage_flag(debt_to_equity_ratio, broad_sector):
    """
    Determine whether a company has high leverage.

    Rules:
    - Financials sector is excluded.
    - Flag only if D/E > 5.
    """

    if debt_to_equity_ratio is None:
        return False

    if broad_sector == "Financials":
        return False

    return debt_to_equity_ratio > 5


def interest_coverage_ratio(
    operating_profit,
    other_income,
    interest,
):
    """
    Calculate Interest Coverage Ratio (ICR).

    Formula:
        (Operating Profit + Other Income) / Interest

    Returns:
        float: Interest Coverage Ratio
        None: If interest is zero
    """

    if interest == 0:
        return None

    return (operating_profit + other_income) / interest


def icr_label(icr):
    """
    Return a display label for Interest Coverage Ratio.

    Returns:
        "Debt Free" if ICR is None.
        Empty string otherwise.
    """

    if icr is None:
        return "Debt Free"

    return ""


def icr_warning_flag(icr):
    """
    Flag companies with weak interest coverage.

    Returns:
        True if ICR < 1.5
        False otherwise
    """

    if icr is None:
        return False

    return icr < 1.5


def net_debt(borrowings, investments):
    """
    Calculate Net Debt.

    Formula:
        Net Debt = Borrowings - Investments

    Returns:
        float: Net Debt
    """

    return borrowings - investments


def asset_turnover(sales, total_assets):
    """
    Calculate Asset Turnover Ratio.

    Formula:
        Asset Turnover = Sales / Total Assets

    Returns:
        float: Asset Turnover Ratio
        None: If total_assets is zero
    """

    if total_assets == 0:
        return None

    return sales / total_assets