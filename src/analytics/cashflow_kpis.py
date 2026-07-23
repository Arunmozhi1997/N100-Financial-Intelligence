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