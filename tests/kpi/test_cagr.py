from src.analytics.cagr import (
    calculate_cagr,
    calculate_cagr_for_window,
    revenue_cagr,
    pat_cagr,
    eps_cagr,
)


def test_calculate_cagr():
    value, flag = calculate_cagr(100, 200, 5)

    assert round(value, 2) == 14.87
    assert flag is None


def test_calculate_cagr_zero_base():
    value, flag = calculate_cagr(0, 200, 5)

    assert value is None
    assert flag == "ZERO_BASE"


def test_calculate_cagr_turnaround():
    value, flag = calculate_cagr(-100, 200, 5)

    assert value is None
    assert flag == "TURNAROUND"


def test_calculate_cagr_decline_to_loss():
    value, flag = calculate_cagr(200, -100, 5)

    assert value is None
    assert flag == "DECLINE_TO_LOSS"


def test_calculate_cagr_both_negative():
    value, flag = calculate_cagr(-200, -100, 5)

    assert value is None
    assert flag == "BOTH_NEGATIVE"


def test_calculate_cagr_insufficient():
    value, flag = calculate_cagr(100, 200, 0)

    assert value is None
    assert flag == "INSUFFICIENT"


def test_revenue_cagr():
    value, flag = revenue_cagr(100, 200, 5)

    assert round(value, 2) == 14.87
    assert flag is None


def test_pat_cagr():
    value, flag = pat_cagr(100, 200, 5)

    assert round(value, 2) == 14.87
    assert flag is None


def test_eps_cagr():
    value, flag = eps_cagr(100, 200, 5)

    assert round(value, 2) == 14.87
    assert flag is None


def test_calculate_cagr_for_window():
    values = [100, 120, 150, 180, 220]

    value, flag = calculate_cagr_for_window(values, 3)

    assert round(value, 2) == 22.39
    assert flag is None


def test_calculate_cagr_for_window_insufficient():
    values = [100, 120]

    value, flag = calculate_cagr_for_window(values, 5)

    assert value is None
    assert flag == "INSUFFICIENT"
