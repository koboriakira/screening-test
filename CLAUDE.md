# 株式スクリーニングシステム

## プロジェクト概要

yfinanceベースの投資分析自動化システム。Claude Code Skillsと組み合わせて、自然言語で投資分析を実行できる。

## アーキテクチャ

3層構造:
- **Skills層** (`/.claude/skills/`): ユーザーインターフェース（5スキル）
- **Core層** (`/src/screening_test/core/`): ビジネスロジック
- **Data層** (`/src/screening_test/data/`): yfinance APIラッパー

## 5つのスキル

1. **screening**: 割安株スクリーニング（4市場、4プリセット）
2. **report**: 個別銘柄の財務分析レポート生成
3. **portfolio**: ポートフォリオ管理（売買記録・損益追跡）
4. **stress_test**: ストレステスト（8シナリオでリスク検証）
5. **watchlist**: ウォッチリスト管理

## データ永続化

- ポートフォリオ: `output/portfolio.csv`
- 取引履歴: `output/transactions.csv`
- ウォッチリスト: `output/watchlist.csv`
- 閾値設定: `config/thresholds.yaml`

## スコアリング基準

バリュースコア（100点満点）:
- PER: 25点（低いほど割安）
- PBR: 25点（低いほど割安）
- 配当利回り: 20点（高いほど高評価）
- ROE: 15点（高いほど高評価）
- 売上成長率: 15点（高いほど高評価）

## 開発コマンド

```bash
uv sync                    # 依存関係のインストール
uv run pytest              # テスト実行
uv run ruff check src/     # リント
uv run ruff format src/    # フォーマット
uv run mypy src/           # 型チェック
uv run screening-test --help  # CLI ヘルプ
```

## 対応市場

- jpx: 日本取引所（東証プライム・スタンダード・グロース）
- us: 米国市場（S&P500等）
- asean: ASEAN市場（シンガポール、インドネシア、タイ、フィリピン）
- hk: 香港市場
