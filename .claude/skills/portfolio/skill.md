# ポートフォリオ管理スキル

売買記録と損益追跡を行うポートフォリオ管理スキル。

## 使い方

ユーザーが「ポートフォリオを見せて」「株を買った」「売却した」「損益を確認」等と指示した場合にこのスキルを使用。

## 実行方法

```bash
cd /home/user/screening-test

# 保有銘柄一覧
uv run screening-test portfolio show

# 株式購入記録
uv run screening-test portfolio buy --ticker {ticker} --shares {shares} --price {price}

# 株式売却記録
uv run screening-test portfolio sell --ticker {ticker} --shares {shares} --price {price}

# ヘルスチェック（現在の評価額と損益）
uv run screening-test portfolio health
```

## パラメータ

- `action`: 操作内容。`show`（一覧）, `buy`（購入）, `sell`（売却）, `health`（ヘルスチェック）
- `ticker`: ティッカーシンボル（buy/sellで必要）
- `shares`: 株数（buy/sellで必要）
- `price`: 価格（buy/sellで必要）

## データ永続化

- ポートフォリオは `output/portfolio.csv` に保存
- 取引履歴は `output/transactions.csv` に保存
- セッション間でデータが維持される

## 使用例

- 「トヨタを100株、3000円で買った」→ `portfolio buy --ticker 7203.T --shares 100 --price 3000`
- 「持ち株の損益を確認して」→ `portfolio health`
