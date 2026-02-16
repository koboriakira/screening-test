"""ウォッチリスト管理のユニットテスト"""

import tempfile
from pathlib import Path
from unittest.mock import patch

from screening_test.core import watchlist


class TestWatchlist:
    """ウォッチリスト操作のテスト"""

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

    def test_show_empty_watchlist(self) -> None:
        result = watchlist.show_watchlist()
        assert "空" in result

    def test_add_to_watchlist(self) -> None:
        result = watchlist.add_to_watchlist("7203.T", "割安に見える")
        assert "追加" in result

    def test_add_and_show(self) -> None:
        watchlist.add_to_watchlist("7203.T", "割安に見える")
        result = watchlist.show_watchlist()
        assert "7203.T" in result
        assert "割安に見える" in result

    def test_add_duplicate(self) -> None:
        watchlist.add_to_watchlist("7203.T", "理由1")
        result = watchlist.add_to_watchlist("7203.T", "理由2")
        assert "すでに" in result

    def test_remove_from_watchlist(self) -> None:
        watchlist.add_to_watchlist("AAPL", "AI期待")
        result = watchlist.remove_from_watchlist("AAPL")
        assert "削除" in result

    def test_remove_nonexistent(self) -> None:
        result = watchlist.remove_from_watchlist("FAKE")
        assert "登録されていません" in result

    def test_manage_watchlist_dispatch(self) -> None:
        result = watchlist.manage_watchlist("show")
        assert "空" in result

    def test_manage_watchlist_add(self) -> None:
        result = watchlist.manage_watchlist("add", ticker="NVDA", reason="AI")
        assert "追加" in result

    def test_manage_watchlist_unknown_action(self) -> None:
        result = watchlist.manage_watchlist("unknown")
        assert "エラー" in result

    def test_manage_watchlist_add_no_ticker(self) -> None:
        result = watchlist.manage_watchlist("add")
        assert "エラー" in result
