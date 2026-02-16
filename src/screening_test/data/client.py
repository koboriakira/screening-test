"""yfinance APIラッパー: キャッシュ、レートリミット、異常値除外を提供"""

import time
from datetime import datetime, timedelta
from typing import Any

import pandas as pd
import yfinance as yf
from pydantic import BaseModel


class StockInfo(BaseModel):
    """銘柄情報のデータモデル"""

    ticker: str
    name: str
    sector: str
    market_cap: float
    per: float | None = None
    pbr: float | None = None
    dividend_yield: float | None = None
    roe: float | None = None
    revenue_growth: float | None = None
    current_price: float | None = None
    fifty_two_week_high: float | None = None
    fifty_two_week_low: float | None = None


class CacheEntry(BaseModel):
    """キャッシュエントリ"""

    data: dict[str, Any]
    expires_at: datetime


class YFinanceClient:
    """yfinance APIクライアント（キャッシュ・レートリミット付き）

    - 24時間TTLのキャッシュ
    - API呼び出し間に1秒のレートリミット
    - 異常値のサニタイズ（配当利回り>15%、PBR<0.1等を除外）
    """

    CACHE_TTL_HOURS = 24
    RATE_LIMIT_SECONDS = 1.0

    # 異常値フィルタ閾値
    MAX_DIVIDEND_YIELD = 15.0
    MIN_PBR = 0.1
    MAX_PER = 200.0
    MIN_PER = 0.0

    def __init__(self) -> None:
        self._cache: dict[str, CacheEntry] = {}
        self._last_call_time: float = 0.0

    def _rate_limit(self) -> None:
        """API呼び出しのレートリミット（1秒間隔）"""
        elapsed = time.monotonic() - self._last_call_time
        if elapsed < self.RATE_LIMIT_SECONDS:
            time.sleep(self.RATE_LIMIT_SECONDS - elapsed)
        self._last_call_time = time.monotonic()

    def _get_cached(self, key: str) -> dict[str, Any] | None:
        """キャッシュからデータを取得（TTL切れならNone）"""
        entry = self._cache.get(key)
        if entry is None:
            return None
        if datetime.now() > entry.expires_at:
            del self._cache[key]
            return None
        return entry.data

    def _set_cache(self, key: str, data: dict[str, Any]) -> None:
        """キャッシュにデータを保存"""
        self._cache[key] = CacheEntry(
            data=data,
            expires_at=datetime.now() + timedelta(hours=self.CACHE_TTL_HOURS),
        )

    def _sanitize_value(self, value: Any, min_val: float | None = None, max_val: float | None = None) -> float | None:
        """異常値のサニタイズ"""
        if value is None or not isinstance(value, (int, float)):
            return None
        val = float(value)
        if min_val is not None and val < min_val:
            return None
        if max_val is not None and val > max_val:
            return None
        return val

    def get_stock_info(self, ticker: str) -> StockInfo | None:
        """銘柄情報を取得（キャッシュ・レートリミット・サニタイズ付き）"""
        cached = self._get_cached(ticker)
        if cached is not None:
            return StockInfo(**cached)

        self._rate_limit()

        try:
            stock = yf.Ticker(ticker)
            info = stock.info
        except Exception:
            return None

        if not info or "shortName" not in info:
            return None

        per = self._sanitize_value(info.get("trailingPE"), min_val=self.MIN_PER, max_val=self.MAX_PER)
        pbr = self._sanitize_value(info.get("priceToBook"), min_val=self.MIN_PBR)
        dividend_yield_raw = info.get("dividendYield")
        dividend_yield_pct = float(dividend_yield_raw) * 100 if dividend_yield_raw is not None else None
        dividend_yield = self._sanitize_value(dividend_yield_pct, max_val=self.MAX_DIVIDEND_YIELD)
        roe_raw = info.get("returnOnEquity")
        roe = float(roe_raw) * 100 if roe_raw is not None else None
        revenue_growth_raw = info.get("revenueGrowth")
        revenue_growth = float(revenue_growth_raw) * 100 if revenue_growth_raw is not None else None

        stock_info_dict = {
            "ticker": ticker,
            "name": info.get("shortName", ""),
            "sector": info.get("sector", ""),
            "market_cap": info.get("marketCap", 0),
            "per": per,
            "pbr": pbr,
            "dividend_yield": dividend_yield,
            "roe": roe,
            "revenue_growth": revenue_growth,
            "current_price": info.get("currentPrice"),
            "fifty_two_week_high": info.get("fiftyTwoWeekHigh"),
            "fifty_two_week_low": info.get("fiftyTwoWeekLow"),
        }

        self._set_cache(ticker, stock_info_dict)
        return StockInfo(**stock_info_dict)

    def get_historical_data(self, ticker: str, period: str = "1y") -> pd.DataFrame:
        """過去の株価データを取得"""
        cache_key = f"{ticker}_hist_{period}"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return pd.DataFrame(cached)

        self._rate_limit()

        try:
            stock = yf.Ticker(ticker)
            df = stock.history(period=period)
            self._set_cache(cache_key, df.to_dict())
            return df
        except Exception:
            return pd.DataFrame()
