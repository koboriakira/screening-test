# screening-test

株式スクリーニングシステム - yfinanceベースの投資分析自動化

## セットアップ

```bash
uv sync
```

## 使い方

```bash
uv run screening-test --help
uv run screening-test screen --market jpx --preset value
uv run screening-test report 7203.T
uv run screening-test portfolio show
uv run screening-test stress 7203.T
uv run screening-test watchlist show
```
