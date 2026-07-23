from src.analytics.ratios import (
    debt_to_equity,
    high_leverage_flag,
    interest_coverage_ratio,
    icr_label,
    icr_warning_flag,
    net_debt,
    asset_turnover,
)

def test_debt_to_equity():
    assert debt_to_equity(200, 100, 300) == 0.5


def test_debt_to_equity_debt_free():
    assert debt_to_equity(0, 100, 300) == 0


def test_debt_to_equity_negative_equity():
    assert debt_to_equity(200, 100, -150) is None


def test_high_leverage_flag_true():
    assert high_leverage_flag(6.2, "Information Technology") is True


def test_high_leverage_flag_false():
    assert high_leverage_flag(3.5, "Information Technology") is False


def test_high_leverage_flag_financials():
    assert high_leverage_flag(8.5, "Financials") is False


def test_high_leverage_flag_none():
    assert high_leverage_flag(None, "Information Technology") is False


def test_interest_coverage_ratio():
    assert interest_coverage_ratio(500, 100, 100) == 6.0


def test_interest_coverage_ratio_zero_interest():
    assert interest_coverage_ratio(500, 100, 0) is None


def test_icr_label_debt_free():
    assert icr_label(None) == "Debt Free"


def test_icr_label_normal():
    assert icr_label(3.2) == ""


def test_icr_warning_flag_true():
    assert icr_warning_flag(1.2) is True


def test_icr_warning_flag_false():
    assert icr_warning_flag(3.5) is False


def test_net_debt():
    assert net_debt(500, 150) == 350


def test_net_debt_negative():
    assert net_debt(300, 500) == -200


def test_asset_turnover():
    assert asset_turnover(1000, 500) == 2.0


def test_asset_turnover_zero_assets():
    assert asset_turnover(1000, 0) is None
