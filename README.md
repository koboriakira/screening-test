# screening-test

株式スクリーニングシステム - yfinanceベースの投資分析自動化

## 概要

yfinance APIを利用した投資分析自動化システム。CLI・MCP(Model Context Protocol)の2つのインターフェースを備え、割安株スクリーニング、財務分析レポート、ポートフォリオ管理、ストレステスト、ウォッチリスト管理の5機能を提供する。

## 必要環境

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) パッケージマネージャ

## セットアップ

```bash
uv sync
```

## 使い方

### CLI

```bash
# ヘルプ
uv run screening-test --help

# 割安株スクリーニング（市場・プリセットを指定）
uv run screening-test screen --market jpx --preset value --top-n 10

# 個別銘柄の財務分析レポート
uv run screening-test report 7203.T

# ポートフォリオ管理
uv run screening-test portfolio show
uv run screening-test portfolio buy --ticker 7203.T --shares 100 --price 2500
uv run screening-test portfolio sell --ticker 7203.T --shares 50 --price 2800

# ストレステスト（8シナリオ）
uv run screening-test stress 7203.T

# ウォッチリスト管理
uv run screening-test watchlist show
uv run screening-test watchlist add --ticker AAPL --reason "割安に見える"
uv run screening-test watchlist remove --ticker AAPL

# バージョン表示
uv run screening-test version
```

### MCP サーバー

Claude Code や他のMCP対応クライアントから自然言語で操作できる。`.mcp.json` の設定により以下の9ツールが利用可能:

| ツール | 説明 |
|--------|------|
| `screen` | 割安株スクリーニング（市場・プリセット・上位N件を指定） |
| `report` | 個別銘柄の財務分析レポート生成 |
| `portfolio_show` | ポートフォリオ一覧の表示 |
| `portfolio_buy` | 株式購入の記録 |
| `portfolio_sell` | 株式売却の記録（損益計算付き） |
| `stress_test` | 8シナリオでのストレステスト |
| `watchlist_show` | ウォッチリスト一覧の表示 |
| `watchlist_add` | ウォッチリストへの銘柄追加 |
| `watchlist_remove` | ウォッチリストからの銘柄削除 |

## 対応市場

| キー | 市場 | 銘柄数 |
|------|------|--------|
| `jpx` | 日本取引所（東証プライム等） | 20 |
| `us` | 米国市場（S&P500等） | 20 |
| `asean` | ASEAN市場（シンガポール、インドネシア、タイ、フィリピン） | 10 |
| `hk` | 香港市場 | 10 |

## スクリーニングプリセット

4つの投資戦略に応じたプリセットを用意。各指標に重み係数をかけてスコアを算出する。

| プリセット | PER | PBR | 配当利回り | ROE | 売上成長率 |
|-----------|-----|-----|-----------|-----|-----------|
| `value`（割安） | 1.5 | 1.5 | 1.0 | 0.5 | 0.5 |
| `growth`（成長） | 0.5 | 0.5 | 0.3 | 1.2 | 1.5 |
| `dividend`（配当） | 0.8 | 0.8 | 1.8 | 0.8 | 0.3 |
| `balanced`（バランス） | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |

## アーキテクチャ

```
src/screening_test/
├── main.py              # CLI（Typer）
├── mcp_server.py        # MCPサーバー（FastMCP）
├── core/                # ビジネスロジック
│   ├── screening.py     #   スクリーニングエンジン
│   ├── scoring.py       #   バリュースコア計算
│   ├── report.py        #   財務分析レポート生成
│   ├── portfolio.py     #   ポートフォリオ管理
│   ├── stress_test.py   #   ストレステスト（8シナリオ）
│   └── watchlist.py     #   ウォッチリスト管理
└── data/                # データアクセス
    ├── client.py        #   yfinance APIラッパー（キャッシュ・レートリミット付き）
    └── tickers.py       #   市場別ティッカーリスト
```

## データ永続化

`output/` ディレクトリに以下のCSVファイルとして保存される（gitignore対象）:

- `portfolio.csv` - 保有銘柄（ティッカー、株数、平均取得単価）
- `transactions.csv` - 取引履歴（日時、売買区分、ティッカー、株数、価格）
- `watchlist.csv` - ウォッチリスト（ティッカー、登録理由、追加日）

## 開発

```bash
uv run pytest              # テスト実行（カバレッジ80%必須）
uv run ruff check src/     # リント
uv run ruff format src/    # フォーマット
uv run mypy src/           # 型チェック
```

## ライセンス

MIT License
