"""ティッカーリストのユニットテスト"""

import pytest

from screening_test.data.tickers import get_tickers


class TestGetTickers:
    """市場別ティッカー取得のテスト"""

    def test_jpx_tickers(self) -> None:
        tickers = get_tickers("jpx")
        assert len(tickers) > 0
        assert all(t.endswith(".T") for t in tickers)

    def test_us_tickers(self) -> None:
        tickers = get_tickers("us")
        assert len(tickers) > 0
        assert "AAPL" in tickers

    def test_asean_tickers(self) -> None:
        tickers = get_tickers("asean")
        assert len(tickers) > 0

    def test_hk_tickers(self) -> None:
        tickers = get_tickers("hk")
        assert len(tickers) > 0
        assert all(t.endswith(".HK") for t in tickers)

    def test_unknown_market_raises(self) -> None:
        with pytest.raises(ValueError, match="不明な市場"):
            get_tickers("invalid")
