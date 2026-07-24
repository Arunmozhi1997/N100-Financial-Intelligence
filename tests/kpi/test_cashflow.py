from src.analytics.cashflow_kpis import (
    free_cash_flow,
    cfo_quality_score,
    capex_intensity,
    fcf_conversion_rate,
    capital_allocation_pattern,
)


def test_free_cash_flow_positive():
    assert free_cash_flow(500, -200) == 300


def test_free_cash_flow_negative():
    assert free_cash_flow(100, -250) == -150


def test_cfo_quality_high():
    ratio, label = cfo_quality_score(120, 100)

    assert ratio == 1.2
    assert label == "High Quality"


def test_cfo_quality_moderate():
    ratio, label = cfo_quality_score(75, 100)

    assert ratio == 0.75
    assert label == "Moderate"


def test_cfo_quality_accrual_risk():
    ratio, label = cfo_quality_score(30, 100)

    assert ratio == 0.3
    assert label == "Accrual Risk"


def test_cfo_quality_zero_pat():
    ratio, label = cfo_quality_score(100, 0)

    assert ratio is None
    assert label is None


def test_capex_asset_light():
    percentage, category = capex_intensity(-20, 1000)

    assert percentage == 2.0
    assert category == "Asset Light"


def test_capex_moderate():
    percentage, category = capex_intensity(-50, 1000)

    assert percentage == 5.0
    assert category == "Moderate"


def test_capex_capital_intensive():
    percentage, category = capex_intensity(-120, 1000)

    assert percentage == 12.0
    assert category == "Capital Intensive"


def test_capex_zero_sales():
    percentage, category = capex_intensity(-100, 0)

    assert percentage is None
    assert category is None


def test_fcf_conversion_rate():
    assert fcf_conversion_rate(300, 500) == 60.0


def test_fcf_conversion_rate_negative():
    assert fcf_conversion_rate(-100, 500) == -20.0


def test_fcf_conversion_rate_zero_operating_profit():
    assert fcf_conversion_rate(300, 0) is None


def test_reinvestor():
    _, _, _, pattern = capital_allocation_pattern(
        500,
        -200,
        -100,
        0.8,
    )

    assert pattern == "Reinvestor"


def test_shareholder_returns():
    _, _, _, pattern = capital_allocation_pattern(
        500,
        -200,
        -100,
        1.3,
    )

    assert pattern == "Shareholder Returns"


def test_liquidating_assets():
    _, _, _, pattern = capital_allocation_pattern(
        500,
        100,
        -50,
    )

    assert pattern == "Liquidating Assets"


def test_distress_signal():
    _, _, _, pattern = capital_allocation_pattern(
        -100,
        50,
        200,
    )

    assert pattern == "Distress Signal"


def test_growth_funded_by_debt():
    _, _, _, pattern = capital_allocation_pattern(
        -200,
        -150,
        400,
    )

    assert pattern == "Growth Funded by Debt"


def test_cash_accumulator():
    _, _, _, pattern = capital_allocation_pattern(
        500,
        100,
        200,
    )

    assert pattern == "Cash Accumulator"


def test_pre_revenue():
    _, _, _, pattern = capital_allocation_pattern(
        -100,
        -100,
        -100,
    )

    assert pattern == "Pre-Revenue"


def test_mixed():
    _, _, _, pattern = capital_allocation_pattern(
        500,
        -200,
        100,
    )

    assert pattern == "Mixed"
