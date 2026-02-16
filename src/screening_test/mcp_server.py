"""MCPサーバー: CLIコマンドをMCPツールとして公開"""

from typing import Any

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("screening-test", instructions="株式スクリーニングシステム - yfinanceベースの投資分析自動化")


@mcp.tool()
def screen(
    market: str = "jpx",
    preset: str = "value",
    top_n: int = 20,
) -> list[dict[str, Any]]:
    """割安株スクリーニングを実行

    対象市場の銘柄をスクリーニングし、スコア上位N銘柄を返します。

    Args:
        market: 対象市場 (jpx: 日本, us: 米国, asean: ASEAN, hk: 香港)
        preset: スクリーニングプリセット (value: 割安, growth: 成長, dividend: 配当, balanced: バランス)
        top_n: 上位N銘柄を返す（デフォルト: 20）
    """
    from screening_test.core.screening import run_screening

    return run_screening(market=market, preset=preset, top_n=top_n)


@mcp.tool()
def report(ticker: str) -> str:
    """個別銘柄の財務分析レポートを生成

    バリュエーション指標、収益性指標、株価情報、バリュースコアを含む詳細レポートを返します。

    Args:
        ticker: 分析対象のティッカーシンボル（例: 7203.T, AAPL）
    """
    from screening_test.core.report import generate_report

    return generate_report(ticker)


@mcp.tool()
def portfolio_show() -> str:
    """ポートフォリオの一覧を表示

    現在保有している銘柄、株数、平均取得単価の一覧を返します。
    """
    from screening_test.core.portfolio import show_portfolio

    return show_portfolio()


@mcp.tool()
def portfolio_buy(ticker: str, shares: int, price: float) -> str:
    """株式の購入を記録

    ポートフォリオに購入記録を追加します。既存銘柄の場合は平均取得単価が再計算されます。

    Args:
        ticker: 購入するティッカーシンボル（例: 7203.T, AAPL）
        shares: 購入株数
        price: 購入単価
    """
    from screening_test.core.portfolio import buy_stock

    return buy_stock(ticker=ticker, shares=shares, price=price)


@mcp.tool()
def portfolio_sell(ticker: str, shares: int, price: float) -> str:
    """株式の売却を記録

    ポートフォリオから売却記録を追加し、損益を計算します。

    Args:
        ticker: 売却するティッカーシンボル（例: 7203.T, AAPL）
        shares: 売却株数
        price: 売却単価
    """
    from screening_test.core.portfolio import sell_stock

    return sell_stock(ticker=ticker, shares=shares, price=price)


@mcp.tool()
def stress_test(ticker: str) -> str:
    """ストレステスト（8シナリオでリスク検証）

    金利上昇、景気後退、パンデミックなど8つのシナリオで、
    指定銘柄の株価への影響をシミュレーションします。

    Args:
        ticker: テスト対象のティッカーシンボル（例: 7203.T, AAPL）
    """
    from screening_test.core.stress_test import run_stress_test

    return run_stress_test(ticker)


@mcp.tool()
def watchlist_show() -> str:
    """ウォッチリストの一覧を表示

    登録されている注目銘柄の一覧（ティッカー、登録理由、追加日）を返します。
    """
    from screening_test.core.watchlist import show_watchlist

    return show_watchlist()


@mcp.tool()
def watchlist_add(ticker: str, reason: str = "") -> str:
    """ウォッチリストに銘柄を追加

    注目銘柄をウォッチリストに登録します。

    Args:
        ticker: 追加するティッカーシンボル（例: 7203.T, AAPL）
        reason: 追加する理由（例: 割安に見える、AI関連で注目）
    """
    from screening_test.core.watchlist import add_to_watchlist

    return add_to_watchlist(ticker=ticker, reason=reason)


@mcp.tool()
def watchlist_remove(ticker: str) -> str:
    """ウォッチリストから銘柄を削除

    指定した銘柄をウォッチリストから削除します。

    Args:
        ticker: 削除するティッカーシンボル（例: 7203.T, AAPL）
    """
    from screening_test.core.watchlist import remove_from_watchlist

    return remove_from_watchlist(ticker=ticker)


if __name__ == "__main__":
    mcp.run()
