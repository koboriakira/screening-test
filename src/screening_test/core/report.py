"""個別銘柄の財務分析レポート生成"""

from screening_test.core.scoring import (
    calculate_value_score,
    score_dividend_yield,
    score_pbr,
    score_per,
    score_revenue_growth,
    score_roe,
)
from screening_test.data.client import YFinanceClient


def generate_report(
    ticker: str,
    client: YFinanceClient | None = None,
) -> str:
    """個別銘柄の財務分析レポートを生成"""
    if client is None:
        client = YFinanceClient()

    info = client.get_stock_info(ticker)
    if info is None:
        return f"エラー: {ticker}のデータを取得できませんでした"

    value_score = calculate_value_score(info)

    lines = [
        f"[bold]{info.name}[/bold] ({info.ticker})",
        f"セクター: {info.sector}",
        f"時価総額: {info.market_cap:,.0f}",
        "",
        "[bold]バリュエーション指標[/bold]",
        f"  PER: {_fmt(info.per, '{:.1f}倍')}  (スコア: {score_per(info.per):.0f}/25)",
        f"  PBR: {_fmt(info.pbr, '{:.2f}倍')}  (スコア: {score_pbr(info.pbr):.0f}/25)",
        "",
        "[bold]収益性指標[/bold]",
        f"  配当利回り: {_fmt(info.dividend_yield, '{:.2f}%')}  (スコア: {score_dividend_yield(info.dividend_yield):.0f}/20)",
        f"  ROE: {_fmt(info.roe, '{:.1f}%')}  (スコア: {score_roe(info.roe):.0f}/15)",
        f"  売上成長率: {_fmt(info.revenue_growth, '{:.1f}%')}  (スコア: {score_revenue_growth(info.revenue_growth):.0f}/15)",
        "",
        "[bold]株価情報[/bold]",
        f"  現在値: {_fmt(info.current_price, '{:,.2f}')}",
        f"  52週高値: {_fmt(info.fifty_two_week_high, '{:,.2f}')}",
        f"  52週安値: {_fmt(info.fifty_two_week_low, '{:,.2f}')}",
        "",
        f"[bold]バリュースコア: {value_score:.1f} / 100[/bold]",
        _score_label(value_score),
    ]
    return "\n".join(lines)


def _fmt(value: float | None, fmt_str: str) -> str:
    """値のフォーマット（Noneの場合は「N/A」）"""
    if value is None:
        return "N/A"
    return fmt_str.format(value)


def _score_label(score: float) -> str:
    """スコアに応じたラベルを返す"""
    if score >= 80:
        return "[bold green]判定: 非常に割安[/bold green]"
    if score >= 60:
        return "[green]判定: 割安[/green]"
    if score >= 40:
        return "[yellow]判定: 適正[/yellow]"
    if score >= 20:
        return "[red]判定: 割高[/red]"
    return "[bold red]判定: 非常に割高[/bold red]"
