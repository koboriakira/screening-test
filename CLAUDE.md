# 株式スクリーニングシステム

## プロジェクト概要

yfinanceベースの投資分析自動化システム。CLI・MCPサーバーの2つのインターフェースを持ち、自然言語での投資分析に対応する。

## アーキテクチャ

3層構造:
- **インターフェース層**: CLI（`main.py` / Typer）、MCPサーバー（`mcp_server.py` / FastMCP）
- **Core層** (`/src/screening_test/core/`): ビジネスロジック
- **Data層** (`/src/screening_test/data/`): yfinance APIラッパー（キャッシュTTL 24時間、レートリミット1秒間隔）

```
src/screening_test/
├── main.py              # CLI（6コマンド: screen, report, portfolio, stress, watchlist, version）
├── mcp_server.py        # MCPサーバー（9ツール）
├── core/
│   ├── screening.py     # スクリーニングエンジン
│   ├── scoring.py       # バリュースコア計算（100点満点）
│   ├── report.py        # 財務分析レポート生成
│   ├── portfolio.py     # ポートフォリオ管理（CSV永続化）
│   ├── stress_test.py   # ストレステスト（8シナリオ × セクター感応度）
│   └── watchlist.py     # ウォッチリスト管理（CSV永続化）
└── data/
    ├── client.py        # YFinanceClient（キャッシュ・レートリミット・異常値フィルタ）
    └── tickers.py       # 市場別ティッカーリスト（計60銘柄）
```

## 5つの機能

1. **screening**: 割安株スクリーニング（4市場 × 4プリセット）
2. **report**: 個別銘柄の財務分析レポート生成
3. **portfolio**: ポートフォリオ管理（売買記録・損益追跡）
4. **stress_test**: ストレステスト（8シナリオでリスク検証）
5. **watchlist**: ウォッチリスト管理

## MCPサーバー

`.mcp.json` で設定。FastMCPベースで以下の9ツールを公開:

`screen`, `report`, `portfolio_show`, `portfolio_buy`, `portfolio_sell`, `stress_test`, `watchlist_show`, `watchlist_add`, `watchlist_remove`

## スコアリング基準

バリュースコア（100点満点）:
- PER: 25点（低いほど割安）
- PBR: 25点（低いほど割安）
- 配当利回り: 20点（高いほど高評価）
- ROE: 15点（高いほど高評価）
- 売上成長率: 15点（高いほど高評価）

### プリセット重み係数

| プリセット | PER | PBR | 配当利回り | ROE | 売上成長率 |
|-----------|-----|-----|-----------|-----|-----------|
| value | 1.5 | 1.5 | 1.0 | 0.5 | 0.5 |
| growth | 0.5 | 0.5 | 0.3 | 1.2 | 1.5 |
| dividend | 0.8 | 0.8 | 1.8 | 0.8 | 0.3 |
| balanced | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |

## ストレステスト8シナリオ

金利上昇、景気後退、為替急変（円高）、パンデミック、地政学リスク、セクターショック、流動性危機、テクノロジーバブル崩壊

セクター感応度で影響を調整（Technology: 1.3, Financial Services: 1.2, Consumer Defensive: 0.6 等）。

## 対応市場

- `jpx`: 日本取引所（20銘柄）
- `us`: 米国市場（20銘柄）
- `asean`: ASEAN市場（10銘柄: シンガポール、インドネシア、タイ、フィリピン）
- `hk`: 香港市場（10銘柄）

## データ永続化

- ポートフォリオ: `output/portfolio.csv`
- 取引履歴: `output/transactions.csv`
- ウォッチリスト: `output/watchlist.csv`
- 閾値設定: `config/thresholds.yaml`

## 異常値フィルタ（サニタイズ）

`config/thresholds.yaml` で設定:
- 配当利回り上限: 15%
- PBR下限: 0.1
- PER範囲: 0〜200

## 開発コマンド

```bash
uv sync                    # 依存関係のインストール
uv run pytest              # テスト実行（カバレッジ80%必須）
uv run ruff check src/     # リント
uv run ruff format src/    # フォーマット
uv run mypy src/           # 型チェック（strictモード）
uv run screening-test --help  # CLI ヘルプ
```

## テスト

- フレームワーク: pytest + pytest-mock + pytest-cov
- カバレッジ: 80%以上必須（`--cov-fail-under=80`）
- マーカー: `slow`, `integration`, `unit`
- テストファイル: `tests/` 配下に8ファイル
