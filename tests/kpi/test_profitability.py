from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets,
    check_opm_difference,
)


def test_net_profit_margin():
    assert net_profit_margin(200, 1000) == 20.0


def test_net_profit_margin_zero_sales():
    assert net_profit_margin(100, 0) is None


def test_operating_profit_margin():
    assert operating_profit_margin(250, 1000) == 25.0


def test_operating_profit_margin_zero_sales():
    assert operating_profit_margin(250, 0) is None

def test_return_on_equity():
    assert return_on_equity(150, 100, 400) == 30.0


def test_return_on_equity_negative_equity():
    assert return_on_equity(100, 100, -150) is None


def test_return_on_capital_employed():
    assert return_on_capital_employed(180, 100, 500, 300) == 20.0


def test_return_on_capital_employed_zero_capital():
    assert return_on_capital_employed(180, -100, -200, 100) is None


def test_return_on_assets():
    assert return_on_assets(120, 1200) == 10.0


def test_return_on_assets_zero_assets():
    assert return_on_assets(120, 0) is None


def test_check_opm_difference_match():
    assert check_opm_difference(25.0, 24.5) is False


def test_check_opm_difference_mismatch():
    assert check_opm_difference(30.0, 27.5) is True


