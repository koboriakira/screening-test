"""ポートフォリオ管理: 売買記録と損益追跡をCSVで永続化"""

import csv
from datetime import datetime
from pathlib import Path

from pydantic import BaseModel

DATA_DIR = Path("output")
PORTFOLIO_FILE = DATA_DIR / "portfolio.csv"
TRANSACTIONS_FILE = DATA_DIR / "transactions.csv"

PORTFOLIO_HEADERS = ["ticker", "shares", "avg_price", "last_updated"]
TRANSACTION_HEADERS = ["date", "action", "ticker", "shares", "price"]


class PortfolioEntry(BaseModel):
    """ポートフォリオの銘柄エントリ"""

    ticker: str
    shares: int
    avg_price: float
    last_updated: str


def _ensure_files() -> None:
    """CSVファイルが存在しない場合はヘッダー付きで作成"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not PORTFOLIO_FILE.exists():
        with PORTFOLIO_FILE.open("w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(PORTFOLIO_HEADERS)
    if not TRANSACTIONS_FILE.exists():
        with TRANSACTIONS_FILE.open("w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(TRANSACTION_HEADERS)


def _load_portfolio() -> dict[str, PortfolioEntry]:
    """ポートフォリオCSVを読み込み"""
    _ensure_files()
    entries: dict[str, PortfolioEntry] = {}
    with PORTFOLIO_FILE.open("r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            entries[row["ticker"]] = PortfolioEntry(
                ticker=row["ticker"],
                shares=int(row["shares"]),
                avg_price=float(row["avg_price"]),
                last_updated=row["last_updated"],
            )
    return entries


def _save_portfolio(entries: dict[str, PortfolioEntry]) -> None:
    """ポートフォリオCSVを保存"""
    _ensure_files()
    with PORTFOLIO_FILE.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=PORTFOLIO_HEADERS)
        writer.writeheader()
        for entry in entries.values():
            writer.writerow(entry.model_dump())


def _record_transaction(action: str, ticker: str, shares: int, price: float) -> None:
    """取引履歴を記録"""
    _ensure_files()
    with TRANSACTIONS_FILE.open("a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().isoformat(), action, ticker, shares, price])


def buy_stock(ticker: str, shares: int, price: float) -> str:
    """株式を購入"""
    entries = _load_portfolio()
    now = datetime.now().isoformat()

    if ticker in entries:
        existing = entries[ticker]
        total_cost = existing.avg_price * existing.shares + price * shares
        total_shares = existing.shares + shares
        entries[ticker] = PortfolioEntry(
            ticker=ticker,
            shares=total_shares,
            avg_price=total_cost / total_shares,
            last_updated=now,
        )
    else:
        entries[ticker] = PortfolioEntry(
            ticker=ticker,
            shares=shares,
            avg_price=price,
            last_updated=now,
        )

    _save_portfolio(entries)
    _record_transaction("buy", ticker, shares, price)
    return f"購入完了: {ticker} x {shares}株 @ {price:.2f}"


def sell_stock(ticker: str, shares: int, price: float) -> str:
    """株式を売却"""
    entries = _load_portfolio()
    if ticker not in entries:
        return f"エラー: {ticker}はポートフォリオに存在しません"

    existing = entries[ticker]
    if existing.shares < shares:
        return f"エラー: 保有株数({existing.shares})が売却株数({shares})より少ないです"

    remaining = existing.shares - shares
    pnl = (price - existing.avg_price) * shares
    now = datetime.now().isoformat()

    if remaining == 0:
        del entries[ticker]
    else:
        entries[ticker] = PortfolioEntry(
            ticker=ticker,
            shares=remaining,
            avg_price=existing.avg_price,
            last_updated=now,
        )

    _save_portfolio(entries)
    _record_transaction("sell", ticker, shares, price)
    return f"売却完了: {ticker} x {shares}株 @ {price:.2f} | 損益: {pnl:+.2f}"


def show_portfolio() -> str:
    """ポートフォリオの一覧を表示"""
    entries = _load_portfolio()
    if not entries:
        return "ポートフォリオは空です"

    lines = ["[bold]現在のポートフォリオ[/bold]\n"]
    lines.append(f"{'ティッカー':12s} {'株数':>8s} {'平均単価':>12s}")
    lines.append("-" * 36)
    for entry in entries.values():
        lines.append(f"{entry.ticker:12s} {entry.shares:>8d} {entry.avg_price:>12.2f}")
    return "\n".join(lines)


def health_check() -> str:
    """ポートフォリオのヘルスチェック"""
    from screening_test.data.client import YFinanceClient

    entries = _load_portfolio()
    if not entries:
        return "ポートフォリオは空です"

    client = YFinanceClient()
    lines = ["[bold]ポートフォリオ ヘルスチェック[/bold]\n"]
    total_value = 0.0
    total_cost = 0.0

    for entry in entries.values():
        info = client.get_stock_info(entry.ticker)
        if info is None or info.current_price is None:
            lines.append(f"{entry.ticker}: データ取得失敗")
            continue

        current_value = info.current_price * entry.shares
        cost_basis = entry.avg_price * entry.shares
        pnl = current_value - cost_basis
        pnl_pct = (pnl / cost_basis) * 100 if cost_basis > 0 else 0

        total_value += current_value
        total_cost += cost_basis

        color = "green" if pnl >= 0 else "red"
        lines.append(
            f"{entry.ticker:10s} | 現在値: {info.current_price:>10.2f} | "
            f"評価額: {current_value:>12.0f} | [{color}]損益: {pnl:>+10.0f} ({pnl_pct:>+.1f}%)[/{color}]"
        )

    total_pnl = total_value - total_cost
    total_pnl_pct = (total_pnl / total_cost) * 100 if total_cost > 0 else 0
    lines.append(f"\n合計評価額: {total_value:,.0f} | 合計損益: {total_pnl:+,.0f} ({total_pnl_pct:+.1f}%)")
    return "\n".join(lines)


def manage_portfolio(
    action: str,
    ticker: str | None = None,
    shares: int | None = None,
    price: float | None = None,
) -> str:
    """ポートフォリオ操作のディスパッチ"""
    if action == "show":
        return show_portfolio()
    if action == "health":
        return health_check()
    if action == "buy":
        if not all([ticker, shares, price]):
            return "エラー: buy操作にはticker, shares, priceが必要です"
        return buy_stock(ticker, shares, price)  # type: ignore[arg-type]
    if action == "sell":
        if not all([ticker, shares, price]):
            return "エラー: sell操作にはticker, shares, priceが必要です"
        return sell_stock(ticker, shares, price)  # type: ignore[arg-type]
    return f"エラー: 不明なアクション '{action}'。利用可能: show, buy, sell, health"
