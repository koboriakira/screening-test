"""ポートフォリオ管理のユニットテスト"""

import tempfile
from pathlib import Path
from unittest.mock import patch

from screening_test.core import portfolio


class TestPortfolio:
    """ポートフォリオ操作のテスト"""

    def setup_method(self) -> None:
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
        self._patch_data_dir = patch.object(portfolio, "DATA_DIR", self.temp_path)
        self._patch_portfolio = patch.object(portfolio, "PORTFOLIO_FILE", self.temp_path / "portfolio.csv")
        self._patch_transactions = patch.object(portfolio, "TRANSACTIONS_FILE", self.temp_path / "transactions.csv")
        self._patch_data_dir.start()
        self._patch_portfolio.start()
        self._patch_transactions.start()

    def teardown_method(self) -> None:
        self._patch_data_dir.stop()
        self._patch_portfolio.stop()
        self._patch_transactions.stop()

    def test_show_empty_portfolio(self) -> None:
        result = portfolio.show_portfolio()
        assert "空" in result

    def test_buy_stock(self) -> None:
        result = portfolio.buy_stock("7203.T", 100, 3000.0)
        assert "購入完了" in result
        assert "7203.T" in result

    def test_buy_and_show(self) -> None:
        portfolio.buy_stock("7203.T", 100, 3000.0)
        result = portfolio.show_portfolio()
        assert "7203.T" in result
        assert "100" in result

    def test_buy_and_sell(self) -> None:
        portfolio.buy_stock("AAPL", 50, 150.0)
        result = portfolio.sell_stock("AAPL", 30, 170.0)
        assert "売却完了" in result
        assert "損益" in result

    def test_sell_all_removes_entry(self) -> None:
        portfolio.buy_stock("AAPL", 50, 150.0)
        portfolio.sell_stock("AAPL", 50, 170.0)
        result = portfolio.show_portfolio()
        assert "空" in result

    def test_sell_nonexistent(self) -> None:
        result = portfolio.sell_stock("FAKE", 10, 100.0)
        assert "エラー" in result

    def test_sell_too_many(self) -> None:
        portfolio.buy_stock("AAPL", 10, 150.0)
        result = portfolio.sell_stock("AAPL", 50, 170.0)
        assert "エラー" in result

    def test_buy_accumulate(self) -> None:
        portfolio.buy_stock("7203.T", 100, 3000.0)
        portfolio.buy_stock("7203.T", 50, 3200.0)
        entries = portfolio._load_portfolio()
        assert entries["7203.T"].shares == 150
        expected_avg = (3000.0 * 100 + 3200.0 * 50) / 150
        assert abs(entries["7203.T"].avg_price - expected_avg) < 0.01

    def test_manage_portfolio_dispatch(self) -> None:
        result = portfolio.manage_portfolio("show")
        assert "空" in result

    def test_manage_portfolio_unknown_action(self) -> None:
        result = portfolio.manage_portfolio("unknown")
        assert "エラー" in result

    def test_manage_portfolio_buy_missing_params(self) -> None:
        result = portfolio.manage_portfolio("buy", ticker="AAPL")
        assert "エラー" in result
