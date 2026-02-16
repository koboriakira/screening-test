"""市場別ティッカーリストの定義"""


def get_jpx_tickers() -> list[str]:
    """JPX（日本取引所）の代表的なティッカーリスト

    実運用ではJPXの銘柄一覧CSVからロードするが、
    ここではデモ用に代表的な銘柄を返す。
    """
    return [
        "7203.T",  # トヨタ自動車
        "6758.T",  # ソニーグループ
        "9984.T",  # ソフトバンクグループ
        "6861.T",  # キーエンス
        "8306.T",  # 三菱UFJフィナンシャル・グループ
        "9432.T",  # 日本電信電話
        "6501.T",  # 日立製作所
        "7741.T",  # HOYA
        "4063.T",  # 信越化学工業
        "8035.T",  # 東京エレクトロン
        "6902.T",  # デンソー
        "4502.T",  # 武田薬品工業
        "6098.T",  # リクルートホールディングス
        "7974.T",  # 任天堂
        "9433.T",  # KDDI
        "6367.T",  # ダイキン工業
        "4661.T",  # オリエンタルランド
        "6594.T",  # 日本電産
        "3382.T",  # セブン&アイ・ホールディングス
        "8058.T",  # 三菱商事
    ]


def get_us_tickers() -> list[str]:
    """米国市場の代表的なティッカーリスト"""
    return [
        "AAPL",
        "MSFT",
        "GOOGL",
        "AMZN",
        "NVDA",
        "META",
        "TSLA",
        "BRK-B",
        "JPM",
        "JNJ",
        "V",
        "PG",
        "UNH",
        "HD",
        "MA",
        "DIS",
        "BAC",
        "XOM",
        "PFE",
        "KO",
    ]


def get_asean_tickers() -> list[str]:
    """ASEAN市場の代表的なティッカーリスト"""
    return [
        "D05.SI",  # DBS Group (Singapore)
        "O39.SI",  # OCBC Bank (Singapore)
        "U11.SI",  # UOB (Singapore)
        "BBCA.JK",  # Bank Central Asia (Indonesia)
        "TLKM.JK",  # Telkom Indonesia
        "BBRI.JK",  # Bank Rakyat Indonesia
        "PTT.BK",  # PTT (Thailand)
        "SCC.BK",  # Siam Cement (Thailand)
        "ADVANC.BK",  # Advanced Info Service (Thailand)
        "TEL.PS",  # PLDT (Philippines)
    ]


def get_hk_tickers() -> list[str]:
    """香港市場の代表的なティッカーリスト"""
    return [
        "0700.HK",  # Tencent
        "9988.HK",  # Alibaba
        "0005.HK",  # HSBC
        "1299.HK",  # AIA Group
        "0941.HK",  # China Mobile
        "2318.HK",  # Ping An Insurance
        "0388.HK",  # HKEX
        "0003.HK",  # CK Infrastructure
        "0001.HK",  # CK Hutchison
        "1398.HK",  # ICBC
    ]


MARKET_TICKERS = {
    "jpx": get_jpx_tickers,
    "us": get_us_tickers,
    "asean": get_asean_tickers,
    "hk": get_hk_tickers,
}


def get_tickers(market: str) -> list[str]:
    """市場名からティッカーリストを取得"""
    getter = MARKET_TICKERS.get(market)
    if getter is None:
        msg = f"不明な市場: {market}。利用可能: {list(MARKET_TICKERS.keys())}"
        raise ValueError(msg)
    return getter()
