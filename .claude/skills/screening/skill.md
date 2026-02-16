# スクリーニングスキル

割安株をスクリーニングするスキル。

## 使い方

ユーザーが「スクリーニングして」「割安株を探して」「銘柄をスクリーニング」等と指示した場合にこのスキルを使用。

## 実行方法

```bash
cd /home/user/screening-test
uv run screening-test screen --market {market} --preset {preset} --top-n {top_n}
```

## パラメータ

- `market`: 対象市場。`jpx`（日本）, `us`（米国）, `asean`（ASEAN）, `hk`（香港）。デフォルト: `jpx`
- `preset`: スクリーニング戦略。`value`（割安）, `growth`（成長）, `dividend`（高配当）, `balanced`（バランス）。デフォルト: `value`
- `top_n`: 表示する上位銘柄数。デフォルト: `20`

## スコアリング基準

バリュースコア（100点満点）:
- PER: 25点（低いほど高スコア）
- PBR: 25点（低いほど高スコア）
- 配当利回り: 20点（高いほど高スコア）
- ROE: 15点（高いほど高スコア）
- 売上成長率: 15点（高いほど高スコア）

## 使用例

- 「日本市場の割安株トップ10」→ `--market jpx --preset value --top-n 10`
- 「米国の高配当株」→ `--market us --preset dividend`
- 「ASEANの成長株を5つ」→ `--market asean --preset growth --top-n 5`
