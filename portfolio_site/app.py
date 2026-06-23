from __future__ import annotations

import html
import os
import sqlite3
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs


BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
DB_PATH = BASE_DIR / "data" / "contacts.db"


def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                company TEXT,
                message TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )


def save_contact(name: str, email: str, company: str, message: str) -> None:
    init_db()
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO contacts (name, email, company, message, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                name,
                email,
                company,
                message,
                datetime.now(timezone.utc).isoformat(timespec="seconds"),
            ),
        )


def render_page(status: str | None = None, errors: list[str] | None = None) -> str:
    alert = ""
    if status == "sent":
        alert = (
            '<div class="alert alert-success" role="status">'
            "お問い合わせを保存しました。折り返しご連絡します。"
            "</div>"
        )
    elif errors:
        items = "".join(f"<li>{html.escape(error)}</li>" for error in errors)
        alert = (
            '<div class="alert alert-error" role="alert">'
            f"<strong>入力内容を確認してください。</strong><ul>{items}</ul>"
            "</div>"
        )

    return f"""<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Alex Mori | Software Engineer Portfolio</title>
  <meta name="description" content="Pythonとクラウドを軸に、使いやすく運用しやすいプロダクトを作るソフトウェアエンジニアのポートフォリオ。">
  <link rel="stylesheet" href="/static/styles.css">
</head>
<body>
  <header class="site-header">
    <a class="brand" href="#top">Alex Mori</a>
    <nav aria-label="Primary navigation">
      <a href="#about">About</a>
      <a href="#work">Work</a>
      <a href="#skills">Skills</a>
      <a href="#contact">Contact</a>
    </nav>
  </header>

  <main id="top">
    <section class="hero section-band">
      <div class="hero-copy">
        <p class="eyebrow">Software Engineer / Python, Cloud, Product UX</p>
        <h1>使いやすさと運用性を両立する、プロダクト志向のエンジニア。</h1>
        <p class="lead">業務システム、API、データ基盤、社内ツールまで。要件の曖昧さを整理し、長く育てられる実装に落とし込みます。</p>
        <div class="hero-actions">
          <a class="button primary" href="#contact">相談する</a>
          <a class="button secondary" href="#work">実績を見る</a>
        </div>
      </div>
      <div class="hero-panel" aria-label="Portfolio highlights">
        <div>
          <span class="metric">8+</span>
          <span class="metric-label">years building products</span>
        </div>
        <div>
          <span class="metric">32%</span>
          <span class="metric-label">average ops cost reduction</span>
        </div>
        <div>
          <span class="metric">12</span>
          <span class="metric-label">teams supported</span>
        </div>
      </div>
    </section>

    <section class="section" id="about">
      <div class="section-heading">
        <p class="eyebrow">About</p>
        <h2>課題発見からリリース後の改善まで伴走します。</h2>
      </div>
      <div class="about-grid">
        <p>バックエンド開発を中心に、顧客体験、開発体験、運用監視をまとめて設計することを得意としています。小さく検証し、計測し、チームが迷わず改善できる状態を作ります。</p>
        <ul class="check-list">
          <li>Python / FastAPI / Django による API 開発</li>
          <li>AWS / Docker / CI/CD を使った運用設計</li>
          <li>SQL / ETL / ダッシュボードによる意思決定支援</li>
        </ul>
      </div>
    </section>

    <section class="section alt" id="work">
      <div class="section-heading">
        <p class="eyebrow">Selected Work</p>
        <h2>代表的なプロジェクト</h2>
      </div>
      <div class="card-grid">
        <article class="card">
          <span class="tag">SaaS</span>
          <h3>契約管理プラットフォーム</h3>
          <p>複雑な承認フローを API とワークキューで再設計。処理時間を短縮し、監査ログを標準化しました。</p>
        </article>
        <article class="card">
          <span class="tag">Data</span>
          <h3>売上分析ダッシュボード</h3>
          <p>散在していた CSV と DB を統合し、日次の意思決定に使える指標とアラートを整備しました。</p>
        </article>
        <article class="card">
          <span class="tag">Internal Tool</span>
          <h3>カスタマーサポート支援ツール</h3>
          <p>問い合わせ履歴とナレッジを横断検索できる UI を実装し、初回応答の品質を安定させました。</p>
        </article>
      </div>
    </section>

    <section class="section" id="skills">
      <div class="section-heading">
        <p class="eyebrow">Skills</p>
        <h2>技術領域</h2>
      </div>
      <div class="skill-list">
        <span>Python</span>
        <span>FastAPI</span>
        <span>Django</span>
        <span>SQLite / PostgreSQL</span>
        <span>AWS</span>
        <span>Docker</span>
        <span>GitHub Actions</span>
        <span>TypeScript</span>
        <span>Product Discovery</span>
      </div>
    </section>

    <section class="section contact-section" id="contact">
      <div class="section-heading">
        <p class="eyebrow">Contact</p>
        <h2>プロジェクトの相談</h2>
        <p>新規開発、既存システム改善、技術相談など、お気軽にご連絡ください。</p>
      </div>
      <form class="contact-form" action="/contact" method="post">
        {alert}
        <label>
          お名前
          <input type="text" name="name" autocomplete="name" required maxlength="120">
        </label>
        <label>
          メールアドレス
          <input type="email" name="email" autocomplete="email" required maxlength="200">
        </label>
        <label>
          会社名・組織名
          <input type="text" name="company" autocomplete="organization" maxlength="160">
        </label>
        <label>
          お問い合わせ内容
          <textarea name="message" rows="6" required maxlength="2000"></textarea>
        </label>
        <button class="button primary" type="submit">送信する</button>
      </form>
    </section>
  </main>

  <footer class="site-footer">
    <p>&copy; 2026 Alex Mori. Built with Python and SQLite.</p>
  </footer>
</body>
</html>"""


def validate_contact(fields: dict[str, str]) -> list[str]:
    errors: list[str] = []
    if not fields["name"]:
        errors.append("お名前を入力してください。")
    if "@" not in fields["email"] or "." not in fields["email"]:
        errors.append("有効なメールアドレスを入力してください。")
    if len(fields["message"]) < 10:
        errors.append("お問い合わせ内容は10文字以上で入力してください。")
    return errors


class PortfolioRequestHandler(BaseHTTPRequestHandler):
    server_version = "PortfolioSite/0.1"

    def do_HEAD(self) -> None:
        if self.path == "/" or self.path.startswith("/?"):
            self.respond_headers(
                len(render_page(status=self.query_status()).encode("utf-8")),
                "text/html; charset=utf-8",
            )
            return
        if self.path == "/static/styles.css":
            self.respond_static_headers(STATIC_DIR / "styles.css", "text/css; charset=utf-8")
            return
        self.send_error(HTTPStatus.NOT_FOUND)

    def do_GET(self) -> None:
        if self.path == "/" or self.path.startswith("/?"):
            self.respond_html(render_page(status=self.query_status()))
            return
        if self.path == "/static/styles.css":
            self.respond_static(STATIC_DIR / "styles.css", "text/css; charset=utf-8")
            return
        self.send_error(HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:
        if self.path != "/contact":
            self.send_error(HTTPStatus.NOT_FOUND)
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(content_length).decode("utf-8")
        parsed = parse_qs(body, keep_blank_values=True)
        fields = {
            "name": parsed.get("name", [""])[0].strip()[:120],
            "email": parsed.get("email", [""])[0].strip()[:200],
            "company": parsed.get("company", [""])[0].strip()[:160],
            "message": parsed.get("message", [""])[0].strip()[:2000],
        }
        errors = validate_contact(fields)
        if errors:
            self.respond_html(render_page(errors=errors), status=HTTPStatus.BAD_REQUEST)
            return

        save_contact(**fields)
        self.send_response(HTTPStatus.SEE_OTHER)
        self.send_header("Location", "/?status=sent#contact")
        self.end_headers()

    def query_status(self) -> str | None:
        if "status=sent" in self.path:
            return "sent"
        return None

    def respond_html(self, content: str, status: HTTPStatus = HTTPStatus.OK) -> None:
        encoded = content.encode("utf-8")
        self.respond_headers(len(encoded), "text/html; charset=utf-8", status)
        self.wfile.write(encoded)

    def respond_static(self, path: Path, content_type: str) -> None:
        if not path.exists():
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        content = path.read_bytes()
        self.respond_headers(len(content), content_type)
        self.wfile.write(content)

    def respond_static_headers(self, path: Path, content_type: str) -> None:
        if not path.exists():
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        self.respond_headers(path.stat().st_size, content_type)

    def respond_headers(
        self,
        content_length: int,
        content_type: str,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(content_length))
        self.end_headers()

    def log_message(self, format: str, *args: object) -> None:
        return


def main() -> None:
    init_db()
    port = int(os.environ.get("PORT", "8000"))
    server = ThreadingHTTPServer(("127.0.0.1", port), PortfolioRequestHandler)
    print(f"Portfolio site running at http://127.0.0.1:{port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
