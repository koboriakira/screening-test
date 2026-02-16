"""ストレステスト: 8シナリオでリスクを検証"""

from pydantic import BaseModel

from screening_test.data.client import YFinanceClient


class ScenarioResult(BaseModel):
    """シナリオ結果"""

    name: str
    description: str
    price_change_pct: float
    estimated_price: float
    impact: str  # "低", "中", "高", "極高"


# 8つのストレステストシナリオ
SCENARIOS = [
    {"name": "金利上昇", "description": "中央銀行が政策金利を1%引き上げ", "shock_pct": -15.0},
    {"name": "景気後退", "description": "GDPが2四半期連続マイナス", "shock_pct": -25.0},
    {"name": "為替急変（円高）", "description": "ドル円が20円下落", "shock_pct": -20.0},
    {"name": "パンデミック", "description": "新たなパンデミックの発生", "shock_pct": -35.0},
    {"name": "地政学リスク", "description": "主要地域での紛争拡大", "shock_pct": -20.0},
    {"name": "セクターショック", "description": "業種特有の規制強化", "shock_pct": -30.0},
    {"name": "流動性危機", "description": "信用市場の急激な収縮", "shock_pct": -25.0},
    {"name": "テクノロジーバブル崩壊", "description": "ハイテク株の大幅調整", "shock_pct": -40.0},
]


def _classify_impact(change_pct: float) -> str:
    """影響度を分類"""
    abs_change = abs(change_pct)
    if abs_change < 10:
        return "低"
    if abs_change < 20:
        return "中"
    if abs_change < 30:
        return "高"
    return "極高"


def run_stress_test(
    ticker: str,
    client: YFinanceClient | None = None,
) -> str:
    """ティッカーに対して8シナリオのストレステストを実行"""
    if client is None:
        client = YFinanceClient()

    info = client.get_stock_info(ticker)
    if info is None or info.current_price is None:
        return f"エラー: {ticker}のデータを取得できませんでした"

    current_price = info.current_price
    results: list[ScenarioResult] = []

    # セクター感応度（セクターによってショックの影響が異なる）
    sector_sensitivity = _get_sector_sensitivity(info.sector)

    for scenario in SCENARIOS:
        adjusted_shock = scenario["shock_pct"] * sector_sensitivity
        estimated_price = current_price * (1 + adjusted_shock / 100)
        result = ScenarioResult(
            name=str(scenario["name"]),
            description=str(scenario["description"]),
            price_change_pct=float(adjusted_shock),
            estimated_price=estimated_price,
            impact=_classify_impact(adjusted_shock),
        )
        results.append(result)

    return _format_results(ticker, current_price, results)


def _get_sector_sensitivity(sector: str) -> float:
    """セクターごとの感応度係数"""
    sensitivity_map = {
        "Technology": 1.3,
        "Financial Services": 1.2,
        "Healthcare": 0.8,
        "Consumer Defensive": 0.6,
        "Utilities": 0.5,
        "Energy": 1.1,
        "Consumer Cyclical": 1.2,
        "Industrials": 1.0,
        "Basic Materials": 1.1,
        "Real Estate": 1.2,
        "Communication Services": 1.0,
    }
    return sensitivity_map.get(sector, 1.0)


def _format_results(ticker: str, current_price: float, results: list[ScenarioResult]) -> str:
    """ストレステスト結果のフォーマット"""
    lines = [
        f"銘柄: {ticker} | 現在値: {current_price:,.2f}\n",
        f"{'シナリオ':20s} {'変動率':>8s} {'予想価格':>12s} {'影響度':>6s}",
        "-" * 52,
    ]

    for r in results:
        impact_color = {"低": "green", "中": "yellow", "高": "red", "極高": "bold red"}.get(r.impact, "white")
        lines.append(
            f"{r.name:20s} {r.price_change_pct:>+7.1f}% {r.estimated_price:>12,.2f} [{impact_color}]{r.impact}[/{impact_color}]"
        )

    worst = min(results, key=lambda x: x.price_change_pct)
    lines.append(f"\n最悪シナリオ: {worst.name} ({worst.price_change_pct:+.1f}%) → {worst.estimated_price:,.2f}")
    return "\n".join(lines)
