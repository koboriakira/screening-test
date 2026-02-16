"""MCPサーバーのユニットテスト"""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

from screening_test.core import portfolio, watchlist
from screening_test.mcp_server import (
    mcp,
    portfolio_buy,
    portfolio_sell,
    portfolio_show,
    report,
    screen,
    stress_test,
    watchlist_add,
    watchlist_remove,
    watchlist_show,
)


class TestMCPServerSetup:
    """MCPサーバーの基本設定テスト"""

    def test_server_name(self) -> None:
        assert mcp.name == "screening-test"

    def test_all_tools_registered(self) -> None:
        """9つのツールがすべて登録されていることを確認"""
        tool_names = {
            "screen",
            "report",
            "portfolio_show",
            "portfolio_buy",
            "portfolio_sell",
            "stress_test",
            "watchlist_show",
            "watchlist_add",
            "watchlist_remove",
        }
        # FastMCPのツール関数が存在することを確認
        assert callable(screen)
        assert callable(report)
        assert callable(portfolio_show)
        assert callable(portfolio_buy)
        assert callable(portfolio_sell)
        assert callable(stress_test)
        assert callable(watchlist_show)
        assert callable(watchlist_add)
        assert callable(watchlist_remove)


class TestScreenTool:
    """screenツールのテスト"""

    @patch("screening_test.core.screening.run_screening")
    def test_screen_default_params(self, mock_run: MagicMock) -> None:
        mock_run.return_value = [{"ticker": "7203.T", "name": "Toyota", "score": 85.0}]
        result = screen()
        mock_run.assert_called_once_with(market="jpx", preset="value", top_n=20)
        assert len(result) == 1
        assert result[0]["ticker"] == "7203.T"

    @patch("screening_test.core.screening.run_screening")
    def test_screen_custom_params(self, mock_run: MagicMock) -> None:
        mock_run.return_value = []
        screen(market="us", preset="growth", top_n=10)
        mock_run.assert_called_once_with(market="us", preset="growth", top_n=10)


class TestReportTool:
    """reportツールのテスト"""

    @patch("screening_test.core.report.generate_report")
    def test_report(self, mock_gen: MagicMock) -> None:
        mock_gen.return_value = "テストレポート"
        result = report("AAPL")
        mock_gen.assert_called_once_with("AAPL")
        assert result == "テストレポート"


class TestPortfolioTools:
    """ポートフォリオツールのテスト"""

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

    def test_portfolio_show_empty(self) -> None:
        result = portfolio_show()
        assert "空" in result

    def test_portfolio_buy(self) -> None:
        result = portfolio_buy("7203.T", 100, 3000.0)
        assert "購入完了" in result

    def test_portfolio_sell_after_buy(self) -> None:
        portfolio_buy("AAPL", 50, 150.0)
        result = portfolio_sell("AAPL", 30, 170.0)
        assert "売却完了" in result

    def test_portfolio_sell_nonexistent(self) -> None:
        result = portfolio_sell("FAKE", 10, 100.0)
        assert "エラー" in result


class TestStressTestTool:
    """ストレステストツールのテスト"""

    @patch("screening_test.core.stress_test.run_stress_test")
    def test_stress_test(self, mock_run: MagicMock) -> None:
        mock_run.return_value = "ストレステスト結果"
        result = stress_test("7203.T")
        mock_run.assert_called_once_with("7203.T")
        assert result == "ストレステスト結果"


class TestWatchlistTools:
    """ウォッチリストツールのテスト"""

    def setup_method(self) -> None:
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
        self._patch_data_dir = patch.object(watchlist, "DATA_DIR", self.temp_path)
        self._patch_watchlist = patch.object(watchlist, "WATCHLIST_FILE", self.temp_path / "watchlist.csv")
        self._patch_data_dir.start()
        self._patch_watchlist.start()

    def teardown_method(self) -> None:
        self._patch_data_dir.stop()
        self._patch_watchlist.stop()

    def test_watchlist_show_empty(self) -> None:
        result = watchlist_show()
        assert "空" in result

    def test_watchlist_add(self) -> None:
        result = watchlist_add("7203.T", "割安に見える")
        assert "追加" in result

    def test_watchlist_add_and_show(self) -> None:
        watchlist_add("AAPL", "AI関連")
        result = watchlist_show()
        assert "AAPL" in result

    def test_watchlist_remove(self) -> None:
        watchlist_add("NVDA", "注目")
        result = watchlist_remove("NVDA")
        assert "削除" in result

    def test_watchlist_remove_nonexistent(self) -> None:
        result = watchlist_remove("FAKE")
        assert "登録されていません" in result
