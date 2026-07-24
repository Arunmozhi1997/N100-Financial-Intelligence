from math import pow


def calculate_cagr(start_value, end_value, years):
    """
    Calculate Compound Annual Growth Rate (CAGR).

    Parameters
    ----------
    start_value : float
        Starting value.
    end_value : float
        Ending value.
    years : int
        Number of years.

    Returns
    -------
    tuple
        (cagr_value, flag)

    Flags
    -----
    None
        Valid CAGR calculated.
    ZERO_BASE
        Starting value is zero.
    TURNAROUND
        Company moved from loss to profit.
    DECLINE_TO_LOSS
        Company moved from profit to loss.
    BOTH_NEGATIVE
        Both start and end values are negative.
    INSUFFICIENT
        Invalid number of years.
    """

    if years <= 0:
        return None, "INSUFFICIENT"

    if start_value == 0:
        return None, "ZERO_BASE"

    if start_value > 0 and end_value < 0:
        return None, "DECLINE_TO_LOSS"

    if start_value < 0 and end_value > 0:
        return None, "TURNAROUND"

    if start_value < 0 and end_value < 0:
        return None, "BOTH_NEGATIVE"

    cagr = (pow(end_value / start_value, 1 / years) - 1) * 100

    return round(cagr, 2), None


def revenue_cagr(start_revenue, end_revenue, years):
    """
    Calculate Revenue CAGR.
    """
    return calculate_cagr(start_revenue, end_revenue, years)


def pat_cagr(start_pat, end_pat, years):
    """
    Calculate Profit After Tax (PAT) CAGR.
    """
    return calculate_cagr(start_pat, end_pat, years)


def eps_cagr(start_eps, end_eps, years):
    """
    Calculate Earnings Per Share (EPS) CAGR.
    """
    return calculate_cagr(start_eps, end_eps, years)


def calculate_cagr_for_window(values, years):
    """
    Calculate CAGR using the last N years of historical values.

    Parameters
    ----------
    values : list
        Historical values ordered from oldest to newest.
    years : int
        Window size (3, 5, or 10).

    Returns
    -------
    tuple
        (cagr_value, flag)
    """

    # Need at least (years + 1) values
    if len(values) < years + 1:
        return None, "INSUFFICIENT"

    start_value = values[-(years + 1)]
    end_value = values[-1]

    return calculate_cagr(start_value, end_value, years)
