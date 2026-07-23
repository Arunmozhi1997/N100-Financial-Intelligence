from math import pow


def calculate_cagr(start_value, end_value, years):
    """
    Calculate Compound Annual Growth Rate (CAGR).

    Returns:
        tuple -> (cagr_value, flag)

    Flags:
        None
        ZERO_BASE
        TURNAROUND
        DECLINE_TO_LOSS
        BOTH_NEGATIVE
        INSUFFICIENT
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

    return cagr, None


def revenue_cagr(start_revenue, end_revenue, years):
    """
    Calculate Revenue CAGR.
    """
    return calculate_cagr(start_revenue, end_revenue, years)


def pat_cagr(start_pat, end_pat, years):
    """
    Calculate PAT CAGR.
    """
    return calculate_cagr(start_pat, end_pat, years)


def eps_cagr(start_eps, end_eps, years):
    """
    Calculate EPS CAGR.
    """
    return calculate_cagr(start_eps, end_eps, years)


def calculate_cagr_for_window(values, years):
    """
    Calculate CAGR for the last N years.

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

    # Need at least (years + 1) data points
    if len(values) < years + 1:
        return None, "INSUFFICIENT"

    start_value = values[-(years + 1)]
    end_value = values[-1]

    return calculate_cagr(start_value, end_value, years)