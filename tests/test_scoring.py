"""スコアリングロジックのユニットテスト"""

import pytest

from screening_test.core.scoring import (
    calculate_preset_score,
    calculate_value_score,
    score_dividend_yield,
    score_pbr,
    score_per,
    score_revenue_growth,
    score_roe,
)
from screening_test.data.client import StockInfo


class TestScorePER:
    """PERスコアのテスト"""

    @pytest.mark.parametrize(
        ("per", "expected"),
        [
            (5.0, 25.0),
            (10.0, 20.0),
            (14.0, 15.0),
            (18.0, 10.0),
            (25.0, 5.0),
            (50.0, 0.0),
            (None, 0.0),
            (-1.0, 0.0),
            (0.0, 0.0),
        ],
    )
    def test_score_per(self, per: float | None, expected: float) -> None:
        assert score_per(per) == expected


class TestScorePBR:
    """PBRスコアのテスト"""

    @pytest.mark.parametrize(
        ("pbr", "expected"),
        [
            (0.3, 25.0),
            (0.7, 20.0),
            (0.9, 15.0),
            (1.2, 10.0),
            (1.8, 5.0),
            (3.0, 0.0),
            (None, 0.0),
            (-0.5, 0.0),
        ],
    )
    def test_score_pbr(self, pbr: float | None, expected: float) -> None:
        assert score_pbr(pbr) == expected


class TestScoreDividendYield:
    """配当利回りスコアのテスト"""

    @pytest.mark.parametrize(
        ("dividend_yield", "expected"),
        [
            (6.0, 20.0),
            (4.5, 16.0),
            (3.5, 12.0),
            (2.5, 8.0),
            (1.5, 4.0),
            (0.5, 0.0),
            (None, 0.0),
            (0.0, 0.0),
        ],
    )
    def test_score_dividend_yield(self, dividend_yield: float | None, expected: float) -> None:
        assert score_dividend_yield(dividend_yield) == expected


class TestScoreROE:
    """ROEスコアのテスト"""

    @pytest.mark.parametrize(
        ("roe", "expected"),
        [
            (25.0, 15.0),
            (17.0, 12.0),
            (12.0, 9.0),
            (8.5, 6.0),
            (6.0, 3.0),
            (2.0, 0.0),
            (None, 0.0),
        ],
    )
    def test_score_roe(self, roe: float | None, expected: float) -> None:
        assert score_roe(roe) == expected


class TestScoreRevenueGrowth:
    """売上成長率スコアのテスト"""

    @pytest.mark.parametrize(
        ("revenue_growth", "expected"),
        [
            (35.0, 15.0),
            (22.0, 12.0),
            (15.0, 9.0),
            (7.0, 6.0),
            (3.0, 3.0),
            (-5.0, 0.0),
            (None, 0.0),
        ],
    )
    def test_score_revenue_growth(self, revenue_growth: float | None, expected: float) -> None:
        assert score_revenue_growth(revenue_growth) == expected


class TestCalculateValueScore:
    """総合バリュースコアのテスト"""

    def test_perfect_score(self) -> None:
        stock = StockInfo(
            ticker="TEST",
            name="Test Corp",
            sector="Technology",
            market_cap=1_000_000_000,
            per=5.0,
            pbr=0.3,
            dividend_yield=6.0,
            roe=25.0,
            revenue_growth=35.0,
        )
        assert calculate_value_score(stock) == 100.0

    def test_zero_score(self) -> None:
        stock = StockInfo(
            ticker="TEST",
            name="Test Corp",
            sector="Technology",
            market_cap=1_000_000_000,
            per=None,
            pbr=None,
            dividend_yield=None,
            roe=None,
            revenue_growth=None,
        )
        assert calculate_value_score(stock) == 0.0

    def test_partial_score(self) -> None:
        stock = StockInfo(
            ticker="TEST",
            name="Test Corp",
            sector="Technology",
            market_cap=1_000_000_000,
            per=10.0,  # 20点
            pbr=1.0,  # 15点
            dividend_yield=3.5,  # 12点
            roe=None,
            revenue_growth=None,
        )
        assert calculate_value_score(stock) == 47.0


class TestCalculatePresetScore:
    """プリセットスコアのテスト"""

    def test_balanced_preset(self) -> None:
        stock = StockInfo(
            ticker="TEST",
            name="Test Corp",
            sector="Technology",
            market_cap=1_000_000_000,
            per=10.0,
            pbr=0.7,
            dividend_yield=3.5,
            roe=12.0,
            revenue_growth=15.0,
        )
        score = calculate_preset_score(stock, "balanced")
        assert 0 <= score <= 100

    def test_value_preset_favors_low_per(self) -> None:
        low_per = StockInfo(
            ticker="LOW",
            name="Low PER",
            sector="",
            market_cap=0,
            per=5.0,
            pbr=1.0,
            dividend_yield=1.0,
            roe=5.0,
            revenue_growth=0.0,
        )
        high_per = StockInfo(
            ticker="HIGH",
            name="High PER",
            sector="",
            market_cap=0,
            per=50.0,
            pbr=1.0,
            dividend_yield=1.0,
            roe=5.0,
            revenue_growth=0.0,
        )
        assert calculate_preset_score(low_per, "value") > calculate_preset_score(high_per, "value")

    def test_unknown_preset_defaults_to_balanced(self) -> None:
        stock = StockInfo(
            ticker="TEST",
            name="Test",
            sector="",
            market_cap=0,
            per=10.0,
            pbr=1.0,
            dividend_yield=3.0,
            roe=10.0,
            revenue_growth=10.0,
        )
        assert calculate_preset_score(stock, "unknown") == calculate_preset_score(stock, "balanced")
