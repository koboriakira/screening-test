# ウォッチリストスキル

注目銘柄を管理するウォッチリストスキル。

## 使い方

ユーザーが「気になる銘柄を登録」「ウォッチリストに追加」「注目銘柄一覧」等と指示した場合にこのスキルを使用。

## 実行方法

```bash
cd /home/user/screening-test

# ウォッチリスト一覧
uv run screening-test watchlist show

# 銘柄追加
uv run screening-test watchlist add --ticker {ticker} --reason "{reason}"

# 銘柄削除
uv run screening-test watchlist remove --ticker {ticker}
```

## パラメータ

- `action`: 操作内容。`show`（一覧）, `add`（追加）, `remove`（削除）
- `ticker`: ティッカーシンボル（add/removeで必要）
- `reason`: ウォッチリストに追加する理由（addで任意）

## データ永続化

- ウォッチリストは `output/watchlist.csv` に保存
- セッション間でデータが維持される

## 使用例

- 「NVIDIAをウォッチリストに追加。AI需要拡大に期待」→ `watchlist add --ticker NVDA --reason "AI需要拡大に期待"`
- 「ウォッチリストを見せて」→ `watchlist show`
- 「トヨタをウォッチリストから外して」→ `watchlist remove --ticker 7203.T`
