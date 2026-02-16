"""バリュースコア計算ロジック

スコア配分:
- PER: 25点（低いほど高スコア）
- PBR: 25点（低いほど高スコア）
- 配当利回り: 20点（高いほど高スコア）
- ROE: 15点（高いほど高スコア）
- 売上成長率: 15点（高いほど高スコア）
"""

from screening_test.data.client import StockInfo


def score_per(per: float | None) -> float:
    """PERスコア（25点満点）: 低いほど割安"""
    if per is None or per <= 0:
        return 0.0
    if per <= 8:
        return 25.0
    if per <= 12:
        return 20.0
    if per <= 15:
        return 15.0
    if per <= 20:
        return 10.0
    if per <= 30:
        return 5.0
    return 0.0


def score_pbr(pbr: float | None) -> float:
    """PBRスコア（25点満点）: 低いほど割安"""
    if pbr is None or pbr <= 0:
        return 0.0
    if pbr <= 0.5:
        return 25.0
    if pbr <= 0.8:
        return 20.0
    if pbr <= 1.0:
        return 15.0
    if pbr <= 1.5:
        return 10.0
    if pbr <= 2.0:
        return 5.0
    return 0.0


def score_dividend_yield(dividend_yield: float | None) -> float:
    """配当利回りスコア（20点満点）: 高いほど高スコア"""
    if dividend_yield is None or dividend_yield <= 0:
        return 0.0
    if dividend_yield >= 5.0:
        return 20.0
    if dividend_yield >= 4.0:
        return 16.0
    if dividend_yield >= 3.0:
        return 12.0
    if dividend_yield >= 2.0:
        return 8.0
    if dividend_yield >= 1.0:
        return 4.0
    return 0.0


def score_roe(roe: float | None) -> float:
    """ROEスコア（15点満点）: 高いほど高スコア"""
    if roe is None:
        return 0.0
    if roe >= 20.0:
        return 15.0
    if roe >= 15.0:
        return 12.0
    if roe >= 10.0:
        return 9.0
    if roe >= 8.0:
        return 6.0
    if roe >= 5.0:
        return 3.0
    return 0.0


def score_revenue_growth(revenue_growth: float | None) -> float:
    """売上成長率スコア（15点満点）: 高いほど高スコア"""
    if revenue_growth is None:
        return 0.0
    if revenue_growth >= 30.0:
        return 15.0
    if revenue_growth >= 20.0:
        return 12.0
    if revenue_growth >= 10.0:
        return 9.0
    if revenue_growth >= 5.0:
        return 6.0
    if revenue_growth >= 0.0:
        return 3.0
    return 0.0


def calculate_value_score(stock: StockInfo) -> float:
    """バリュースコアの総合計算（100点満点）"""
    return (
        score_per(stock.per)
        + score_pbr(stock.pbr)
        + score_dividend_yield(stock.dividend_yield)
        + score_roe(stock.roe)
        + score_revenue_growth(stock.revenue_growth)
    )


PRESET_WEIGHTS = {
    "value": {"per": 1.5, "pbr": 1.5, "dividend_yield": 1.0, "roe": 0.5, "revenue_growth": 0.5},
    "growth": {"per": 0.5, "pbr": 0.5, "dividend_yield": 0.3, "roe": 1.2, "revenue_growth": 1.5},
    "dividend": {"per": 0.8, "pbr": 0.8, "dividend_yield": 1.8, "roe": 0.8, "revenue_growth": 0.3},
    "balanced": {"per": 1.0, "pbr": 1.0, "dividend_yield": 1.0, "roe": 1.0, "revenue_growth": 1.0},
}


def calculate_preset_score(stock: StockInfo, preset: str = "balanced") -> float:
    """プリセットに基づくスコア計算"""
    weights = PRESET_WEIGHTS.get(preset, PRESET_WEIGHTS["balanced"])
    raw_scores = {
        "per": score_per(stock.per),
        "pbr": score_pbr(stock.pbr),
        "dividend_yield": score_dividend_yield(stock.dividend_yield),
        "roe": score_roe(stock.roe),
        "revenue_growth": score_revenue_growth(stock.revenue_growth),
    }
    weighted_sum = sum(raw_scores[k] * weights[k] for k in raw_scores)
    weight_total = sum(weights.values())
    return (weighted_sum / weight_total) * (100 / 20)  # 100点満点にスケーリング
