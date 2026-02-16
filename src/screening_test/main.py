"""CLIエントリポイント: Typerベースのコマンドラインインターフェース"""

import typer
from rich.console import Console
from rich.panel import Panel

from screening_test import __version__

app = typer.Typer(name="screening-test", help="株式スクリーニングシステム")
console = Console()


@app.command()
def screen(
    market: str = typer.Option("jpx", help="対象市場 (jpx, us, asean, hk)"),
    preset: str = typer.Option("value", help="スクリーニングプリセット (value, growth, dividend, balanced)"),
    top_n: int = typer.Option(20, help="上位N銘柄を表示"),
) -> None:
    """割安株スクリーニングを実行"""
    from screening_test.core.screening import run_screening

    results = run_screening(market=market, preset=preset, top_n=top_n)
    for rank, stock in enumerate(results, 1):
        console.print(f"[bold]{rank:3d}.[/bold] {stock['ticker']:10s} | スコア: {stock['score']:.1f} | {stock['name']}")


@app.command()
def report(
    ticker: str = typer.Argument(help="分析対象のティッカーシンボル"),
) -> None:
    """個別銘柄の財務分析レポートを生成"""
    from screening_test.core.report import generate_report

    result = generate_report(ticker)
    console.print(Panel(result, title=f"[bold blue]{ticker} 分析レポート[/bold blue]", border_style="blue"))


@app.command()
def portfolio(
    action: str = typer.Argument(help="操作 (show, buy, sell, health)"),
    ticker: str = typer.Option(None, help="ティッカーシンボル"),
    shares: int = typer.Option(None, help="株数"),
    price: float = typer.Option(None, help="価格"),
) -> None:
    """ポートフォリオ管理"""
    from screening_test.core.portfolio import manage_portfolio

    result = manage_portfolio(action=action, ticker=ticker, shares=shares, price=price)
    console.print(result)


@app.command()
def stress(
    ticker: str = typer.Argument(help="ストレステスト対象のティッカーシンボル"),
) -> None:
    """ストレステスト（8シナリオでリスク検証）"""
    from screening_test.core.stress_test import run_stress_test

    results = run_stress_test(ticker)
    console.print(Panel(results, title=f"[bold red]{ticker} ストレステスト[/bold red]", border_style="red"))


@app.command()
def watchlist(
    action: str = typer.Argument(help="操作 (show, add, remove)"),
    ticker: str = typer.Option(None, help="ティッカーシンボル"),
    reason: str = typer.Option(None, help="ウォッチリストに追加する理由"),
) -> None:
    """ウォッチリスト管理"""
    from screening_test.core.watchlist import manage_watchlist

    result = manage_watchlist(action=action, ticker=ticker, reason=reason)
    console.print(result)


@app.command()
def version() -> None:
    """バージョン情報を表示"""
    console.print(f"screening-test v{__version__}")


if __name__ == "__main__":
    app()
