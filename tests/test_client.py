"""yfinanceクライアントのユニットテスト"""

from datetime import datetime, timedelta
from typing import Any

from screening_test.data.client import CacheEntry, StockInfo, YFinanceClient


class TestStockInfo:
    """StockInfoモデルのテスト"""

    def test_create_with_all_fields(self) -> None:
        info = StockInfo(
            ticker="7203.T",
            name="Toyota Motor",
            sector="Consumer Cyclical",
            market_cap=30_000_000_000_000,
            per=10.5,
            pbr=1.2,
            dividend_yield=2.5,
            roe=12.0,
            revenue_growth=8.0,
            current_price=2500.0,
            fifty_two_week_high=3000.0,
            fifty_two_week_low=2000.0,
        )
        assert info.ticker == "7203.T"
        assert info.per == 10.5

    def test_create_with_optional_none(self) -> None:
        info = StockInfo(
            ticker="TEST",
            name="Test",
            sector="",
            market_cap=0,
        )
        assert info.per is None
        assert info.pbr is None
        assert info.dividend_yield is None


class TestYFinanceClient:
    """YFinanceClientのテスト"""

    def setup_method(self) -> None:
        self.client = YFinanceClient()

    def test_sanitize_value_within_range(self) -> None:
        assert self.client._sanitize_value(10.0, min_val=0.0, max_val=100.0) == 10.0

    def test_sanitize_value_below_min(self) -> None:
        assert self.client._sanitize_value(0.05, min_val=0.1) is None

    def test_sanitize_value_above_max(self) -> None:
        assert self.client._sanitize_value(20.0, max_val=15.0) is None

    def test_sanitize_value_none(self) -> None:
        assert self.client._sanitize_value(None) is None

    def test_sanitize_value_non_numeric(self) -> None:
        assert self.client._sanitize_value("not a number") is None  # type: ignore[arg-type]

    def test_cache_set_and_get(self) -> None:
        data: dict[str, Any] = {"ticker": "TEST", "value": 42}
        self.client._set_cache("test_key", data)
        cached = self.client._get_cached("test_key")
        assert cached == data

    def test_cache_miss(self) -> None:
        assert self.client._get_cached("nonexistent") is None

    def test_cache_expired(self) -> None:
        self.client._cache["expired_key"] = CacheEntry(
            data={"value": 1},
            expires_at=datetime.now() - timedelta(hours=1),
        )
        assert self.client._get_cached("expired_key") is None
        assert "expired_key" not in self.client._cache
