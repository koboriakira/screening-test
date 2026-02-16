"""スクリーニングエンジン: 複数のスクリーニング戦略を提供"""

from typing import Any

from rich.console import Console

from screening_test.core.scoring import calculate_preset_score
from screening_test.data.client import YFinanceClient
from screening_test.data.tickers import get_tickers

console = Console()


def _fetch_and_score(
    client: YFinanceClient,
    tickers: list[str],
    preset: str,
) -> list[dict[str, Any]]:
    """ティッカーリストからデータ取得・スコア計算"""
    results: list[dict[str, Any]] = []
    for ticker in tickers:
        info = client.get_stock_info(ticker)
        if info is None:
            continue
        score = calculate_preset_score(info, preset)
        results.append(
            {
                "ticker": info.ticker,
                "name": info.name,
                "score": score,
                "per": info.per,
                "pbr": info.pbr,
                "dividend_yield": info.dividend_yield,
                "roe": info.roe,
                "revenue_growth": info.revenue_growth,
            }
        )
    return results


def run_screening(
    market: str = "jpx",
    preset: str = "value",
    top_n: int = 20,
    client: YFinanceClient | None = None,
) -> list[dict[str, Any]]:
    """スクリーニングを実行し、上位N銘柄を返す

    Args:
        market: 対象市場 (jpx, us, asean, hk)
        preset: スクリーニングプリセット (value, growth, dividend, balanced)
        top_n: 上位N銘柄を返す
        client: YFinanceClient（テスト用にDI可能）

    Returns:
        スコア順にソートされた銘柄情報のリスト
    """
    if client is None:
        client = YFinanceClient()

    tickers = get_tickers(market)
    console.print(f"[dim]市場: {market} | プリセット: {preset} | 銘柄数: {len(tickers)}[/dim]")

    results = _fetch_and_score(client, tickers, preset)
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_n]


def screen_by_criteria(
    tickers: list[str],
    min_score: float = 50.0,
    preset: str = "balanced",
    client: YFinanceClient | None = None,
) -> list[dict[str, Any]]:
    """最低スコア基準でのフィルタリング"""
    if client is None:
        client = YFinanceClient()

    results = _fetch_and_score(client, tickers, preset)
    filtered = [r for r in results if r["score"] >= min_score]
    filtered.sort(key=lambda x: x["score"], reverse=True)
    return filtered
