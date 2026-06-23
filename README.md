# sample_app

Python で作ったエンジニア向けの 1 ページポートフォリオサイトです。
問い合わせフォームの送信内容は SQLite に保存されます。

## Requirements

- Python 3.12+
- uv

## Run

```bash
uv run python -m portfolio_site.app
```

ブラウザで <http://127.0.0.1:8000> を開いてください。

## Database

問い合わせ内容は `data/contacts.db` の `contacts` テーブルに保存されます。
