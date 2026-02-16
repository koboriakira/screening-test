"""ウォッチリスト管理: 注目銘柄の追跡をCSVで永続化"""

import csv
from datetime import datetime
from pathlib import Path

from pydantic import BaseModel

DATA_DIR = Path("output")
WATCHLIST_FILE = DATA_DIR / "watchlist.csv"

WATCHLIST_HEADERS = ["ticker", "reason", "added_at"]


class WatchlistEntry(BaseModel):
    """ウォッチリストエントリ"""

    ticker: str
    reason: str
    added_at: str


def _ensure_file() -> None:
    """CSVファイルが存在しない場合はヘッダー付きで作成"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not WATCHLIST_FILE.exists():
        with WATCHLIST_FILE.open("w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(WATCHLIST_HEADERS)


def _load_watchlist() -> list[WatchlistEntry]:
    """ウォッチリストCSVを読み込み"""
    _ensure_file()
    entries: list[WatchlistEntry] = []
    with WATCHLIST_FILE.open("r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            entries.append(
                WatchlistEntry(
                    ticker=row["ticker"],
                    reason=row["reason"],
                    added_at=row["added_at"],
                )
            )
    return entries


def _save_watchlist(entries: list[WatchlistEntry]) -> None:
    """ウォッチリストCSVを保存"""
    _ensure_file()
    with WATCHLIST_FILE.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=WATCHLIST_HEADERS)
        writer.writeheader()
        for entry in entries:
            writer.writerow(entry.model_dump())


def add_to_watchlist(ticker: str, reason: str = "") -> str:
    """ウォッチリストに銘柄を追加"""
    entries = _load_watchlist()
    existing_tickers = {e.ticker for e in entries}

    if ticker in existing_tickers:
        return f"{ticker}はすでにウォッチリストに登録されています"

    entries.append(
        WatchlistEntry(
            ticker=ticker,
            reason=reason,
            added_at=datetime.now().isoformat(),
        )
    )
    _save_watchlist(entries)
    return f"ウォッチリストに追加: {ticker}"


def remove_from_watchlist(ticker: str) -> str:
    """ウォッチリストから銘柄を削除"""
    entries = _load_watchlist()
    new_entries = [e for e in entries if e.ticker != ticker]

    if len(new_entries) == len(entries):
        return f"{ticker}はウォッチリストに登録されていません"

    _save_watchlist(new_entries)
    return f"ウォッチリストから削除: {ticker}"


def show_watchlist() -> str:
    """ウォッチリストの一覧を表示"""
    entries = _load_watchlist()
    if not entries:
        return "ウォッチリストは空です"

    lines = ["[bold]ウォッチリスト[/bold]\n"]
    lines.append(f"{'ティッカー':12s} {'理由':30s} {'追加日'}")
    lines.append("-" * 70)
    for entry in entries:
        date_str = entry.added_at[:10]
        lines.append(f"{entry.ticker:12s} {entry.reason:30s} {date_str}")
    return "\n".join(lines)


def manage_watchlist(
    action: str,
    ticker: str | None = None,
    reason: str | None = None,
) -> str:
    """ウォッチリスト操作のディスパッチ"""
    if action == "show":
        return show_watchlist()
    if action == "add":
        if ticker is None:
            return "エラー: add操作にはtickerが必要です"
        return add_to_watchlist(ticker, reason or "")
    if action == "remove":
        if ticker is None:
            return "エラー: remove操作にはtickerが必要です"
        return remove_from_watchlist(ticker)
    return f"エラー: 不明なアクション '{action}'。利用可能: show, add, remove"
