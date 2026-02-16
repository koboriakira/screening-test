"""ストレステストのユニットテスト"""

import pytest

from screening_test.core.stress_test import SCENARIOS, _classify_impact, _get_sector_sensitivity


class TestClassifyImpact:
    """影響度分類のテスト"""

    @pytest.mark.parametrize(
        ("change_pct", "expected"),
        [
            (-5.0, "低"),
            (-15.0, "中"),
            (-25.0, "高"),
            (-35.0, "極高"),
        ],
    )
    def test_classify_impact(self, change_pct: float, expected: str) -> None:
        assert _classify_impact(change_pct) == expected


class TestSectorSensitivity:
    """セクター感応度のテスト"""

    def test_technology_high_sensitivity(self) -> None:
        assert _get_sector_sensitivity("Technology") == 1.3

    def test_consumer_defensive_low_sensitivity(self) -> None:
        assert _get_sector_sensitivity("Consumer Defensive") == 0.6

    def test_unknown_sector_default(self) -> None:
        assert _get_sector_sensitivity("Unknown Sector") == 1.0


class TestScenarios:
    """シナリオ定義のテスト"""

    def test_eight_scenarios(self) -> None:
        assert len(SCENARIOS) == 8

    def test_all_scenarios_have_required_fields(self) -> None:
        for scenario in SCENARIOS:
            assert "name" in scenario
            assert "description" in scenario
            assert "shock_pct" in scenario

    def test_all_shocks_negative(self) -> None:
        for scenario in SCENARIOS:
            assert scenario["shock_pct"] < 0
