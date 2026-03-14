"""
StratIQ Server — Flask backend
Serves the frontend, scrapes URLs for browser-side AI, manages SQLite session history.

Endpoints:
  GET  /                        → serves stratiq_8.html
  POST /api/scrape              → fetch company pages, return clean text (no AI — browser does AI)
  POST /api/scan/save           → persist browser-computed scan results to SQLite
  POST /api/scan                → legacy alias for /api/scrape
  POST /api/generate            → save browser-computed strategy results to SQLite
  GET  /api/sessions            → list all saved sessions
  GET  /api/session/<id>        → load a session
  POST /api/session/<id>/save   → save/update session data
  DELETE /api/session/<id>      → delete a session
  GET  /api/health              → health check
"""

import os
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import json
import uuid
import sqlite3
import traceback
from datetime import datetime, timezone
from urllib.parse import urlparse
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests as http_requests
from bs4 import BeautifulSoup

# providers/ imports removed — AI calls are browser-direct, Flask only scrapes + SQLite

# ── Scraping helpers ──────────────────────────────────────────────────────────
SCRAPE_TIMEOUT = 15
MAX_CHARS = 12000
SCRAPE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

def _clean(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script","style","noscript","iframe","svg","img",
                     "header","footer","nav","aside","form","button","meta","link","head"]):
        tag.decompose()
    lines = [l.strip() for l in soup.get_text(separator="\n", strip=True).splitlines() if l.strip()]
    return "\n".join(lines)[:MAX_CHARS]

def _fetch_page(url: str) -> dict:
    for verify in (True, False):
        try:
            r = http_requests.get(url, headers=SCRAPE_HEADERS, timeout=SCRAPE_TIMEOUT,
                                  allow_redirects=True, verify=verify)
            r.raise_for_status()
            return {"url": url, "status": "ok", "content": _clean(r.text)}
        except Exception as e:
            if verify:
                continue
            return {"url": url, "status": "error", "content": "", "error": str(e)}
    return {"url": url, "status": "error", "content": "", "error": "fetch failed"}

# Keywords to match against hrefs when crawling homepage links
_ABOUT_KEYS      = ["about", "who-we-are", "about-us", "company", "overview", "our-story", "our-journey", "our-history", "history"]
_NEWS_KEYS       = ["news", "press", "media", "blog", "insights", "updates", "announcements"]
_LEADERSHIP_KEYS = ["leadership", "team", "management", "executives", "board", "our-team", "directors", "our-history", "history", "founders", "people", "governance", "senior"]

def _candidate_urls(base: str) -> dict:
    """Fetch homepage, crawl its links, find best match for each page type."""
    if not base.startswith("http"):
        base = "https://" + base
    p = urlparse(base)
    root = f"{p.scheme}://{p.netloc}"

    # Fetch homepage HTML and extract all internal links
    try:
        resp = http_requests.get(base, timeout=15, verify=False,
                                 headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "lxml")
        links = []
        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            if href.startswith("/"):
                href = root + href
            elif not href.startswith("http"):
                continue
            # Only internal links
            if urlparse(href).netloc == p.netloc:
                links.append(href.rstrip("/").lower())
        links = list(dict.fromkeys(links))  # dedupe, preserve order
    except Exception:
        links = []

    def best_match(keys):
        for key in keys:
            for link in links:
                path = urlparse(link).path.lower()
                if key in path:
                    return link
        return None

    about_url      = best_match(_ABOUT_KEYS)      or root + "/about"
    news_url       = best_match(_NEWS_KEYS)        or root + "/news"
    leadership_url = best_match(_LEADERSHIP_KEYS) or root + "/leadership"

    return {
        "homepage":   base,
        "about":      about_url,
        "news":       news_url,
        "leadership": leadership_url,
    }

# ── Config ────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = BASE_DIR
DB_PATH = os.environ.get("STRATIQ_DB", os.path.join(BASE_DIR, "data", "stratiq.db"))
PORT = int(os.environ.get("PORT", 3000))

app = Flask(__name__, static_folder=STATIC_DIR)
CORS(app)

# ── Database ──────────────────────────────────────────────────────────────────

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with get_db() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS sessions (
                id          TEXT PRIMARY KEY,
                company_name TEXT NOT NULL DEFAULT 'Unknown',
                url         TEXT,
                provider    TEXT,
                status      TEXT DEFAULT 'draft',
                created_at  TEXT NOT NULL,
                updated_at  TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS session_data (
                id          TEXT PRIMARY KEY,
                session_id  TEXT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
                data_type   TEXT NOT NULL,
                version     INTEGER DEFAULT 1,
                payload     TEXT NOT NULL,
                created_at  TEXT NOT NULL,
                UNIQUE(session_id, data_type, version)
            );

            CREATE TABLE IF NOT EXISTS audit_log (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id  TEXT,
                action      TEXT NOT NULL,
                detail      TEXT,
                created_at  TEXT NOT NULL
            );

            CREATE INDEX IF NOT EXISTS idx_session_data_session ON session_data(session_id);
            CREATE INDEX IF NOT EXISTS idx_audit_session ON audit_log(session_id);
        """)

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def log_action(conn, session_id: str, action: str, detail: str = None):
    conn.execute(
        "INSERT INTO audit_log (session_id, action, detail, created_at) VALUES (?, ?, ?, ?)",
        (session_id, action, detail, now_iso())
    )

# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return send_from_directory(STATIC_DIR, "stratiq_8.html")

@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "version": "1.0.0"})

# ── AI Proxy (browser → Flask → AI provider) ─────────────────────────────────
# Browser cannot reach api.anthropic.com directly (network-level block).
# Flask on localhost can (curl proves it). All AI calls route through here.

@app.route("/api/ai", methods=["POST"])
def ai_proxy():
    body = request.get_json(force=True)
    provider_name = (body.get("provider") or "anthropic").lower()
    api_key = (body.get("api_key") or "").strip()
    messages = body.get("messages", [])
    system = body.get("system", "")
    max_tokens = int(body.get("max_tokens", 4000))

    if not api_key:
        return jsonify({"error": "api_key is required"}), 400
    if not messages:
        return jsonify({"error": "messages is required"}), 400

    try:
        text = _ai_call(provider_name, api_key, messages, system, max_tokens)
        return jsonify({"text": text})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 502


def _build_provider_payload(provider: str, api_key: str, messages: list, system: str, max_tokens: int) -> dict:
    """Build the payload for each provider."""
    if provider == "anthropic":
        payload = {"model": "claude-sonnet-4-6", "max_tokens": max_tokens, "messages": messages}
        if system and system.strip():
            payload["system"] = system.strip()
    elif provider == "openai":
        msgs = ([{"role": "system", "content": system}] if system else []) + messages
        payload = {"model": "gpt-4o", "max_tokens": max_tokens, "messages": msgs}
    elif provider == "google":
        parts = [{"text": m["content"]} for m in messages if m.get("role") == "user"]
        if system:
            parts.insert(0, {"text": system})
        payload = {"contents": [{"parts": parts}], "generationConfig": {"maxOutputTokens": max_tokens}}
    elif provider == "openrouter":
        msgs = ([{"role": "system", "content": system}] if system else []) + messages
        payload = {"model": "anthropic/claude-sonnet-4-5", "max_tokens": max_tokens, "messages": msgs}
    else:
        raise ValueError(f"Unknown provider: {provider}")
    return payload


def _extract_text(provider: str, data: dict) -> str:
    if provider == "anthropic":
        if "error" in data:
            raise RuntimeError(data["error"].get("message", str(data["error"])))
        return "\n".join(b["text"] for b in data.get("content", []) if b.get("type") == "text")
    elif provider == "google":
        return data["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return data["choices"][0]["message"]["content"]


def _ai_call(provider: str, api_key: str, messages: list, system: str, max_tokens: int) -> str:
    """Route AI call through Node proxy on host (host.docker.internal:3001).
    MDE blocks Python/Docker TLS to AI providers but Node on the host works fine."""
    payload = _build_provider_payload(provider, api_key, messages, system, max_tokens)
    proxy_url = "http://host.docker.internal:3001/proxy"
    r = http_requests.post(proxy_url, json={"provider": provider, "api_key": api_key, "payload": payload}, timeout=120)
    r.raise_for_status()
    data = r.json()
    if "error" in data:
        raise RuntimeError(data["error"])
    return _extract_text(provider, data)


# ── Scrape (browser calls this, then does AI itself) ─────────────────────────

@app.route("/api/scrape", methods=["POST"])
def scrape():
    """
    Fetch company pages and return clean text.
    No AI call here — browser sends this content to Claude directly.
    Avoids Docker network isolation issue on Mac.
    """
    body = request.get_json(force=True)
    url = (body.get("url") or "").strip()
    if not url:
        return jsonify({"error": "url is required"}), 400

    pages = _candidate_urls(url)
    results = {}
    for key, page_url in pages.items():
        results[key] = _fetch_page(page_url)

    return jsonify({"base_url": url, "pages": results})


@app.route("/api/scan/save", methods=["POST"])
def scan_save():
    """
    Save browser-computed scan results (company profile + signals) to SQLite.
    Called after browser finishes AI extraction.
    """
    body = request.get_json(force=True)
    url = (body.get("url") or "").strip()
    provider_name = (body.get("provider") or "anthropic").lower()
    result = body.get("result", {})
    session_id = body.get("session_id") or str(uuid.uuid4())
    company_name = result.get("company", {}).get("name", "Unknown Organisation")

    try:
        with get_db() as conn:
            existing = conn.execute("SELECT id FROM sessions WHERE id=?", (session_id,)).fetchone()
            if existing:
                conn.execute(
                    "UPDATE sessions SET company_name=?, url=?, provider=?, updated_at=? WHERE id=?",
                    (company_name, url, provider_name, now_iso(), session_id)
                )
            else:
                conn.execute(
                    "INSERT INTO sessions (id, company_name, url, provider, status, created_at, updated_at) VALUES (?,?,?,?,?,?,?)",
                    (session_id, company_name, url, provider_name, "scanning", now_iso(), now_iso())
                )
            _upsert_session_data(conn, session_id, "scan", result)
            log_action(conn, session_id, "scan_complete", f"Scanned {url} via {provider_name}")

        return jsonify({"ok": True, "session_id": session_id})

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Save failed: {str(e)}"}), 500


# ── Scan (legacy — kept for compatibility, now just calls scrape) ─────────────

@app.route("/api/scan", methods=["POST"])
def scan():
    """Legacy endpoint — redirects to scrape. AI call must happen browser-side."""
    body = request.get_json(force=True)
    url = (body.get("url") or "").strip()
    if not url:
        return jsonify({"error": "url is required"}), 400
    pages = _candidate_urls(url)
    results = {}
    for key, page_url in pages.items():
        results[key] = _fetch_page(page_url)
    return jsonify({
        "base_url": url,
        "pages": results,
        "_note": "AI extraction must be done browser-side. Use /api/scan/save to persist results."
    })

# ── Generate ─────────────────────────────────────────────────────────────────

@app.route("/api/generate", methods=["POST"])
def generate():
    """
    Receives pre-computed AI results from the browser and saves them to SQLite.
    AI calls happen browser-side to avoid Docker network limitations.
    """
    body = request.get_json(force=True)
    session_id = body.get("session_id") or str(uuid.uuid4())
    provider_name = (body.get("provider") or "anthropic").lower()
    company_name = body.get("company_name", "Organisation")
    url = body.get("url", "")

    try:
        with get_db() as conn:
            existing = conn.execute("SELECT id FROM sessions WHERE id=?", (session_id,)).fetchone()
            if not existing:
                conn.execute(
                    "INSERT INTO sessions (id, company_name, url, provider, status, created_at, updated_at) VALUES (?,?,?,?,?,?,?)",
                    (session_id, company_name, url, provider_name, "complete", now_iso(), now_iso())
                )
            else:
                conn.execute(
                    "UPDATE sessions SET status='complete', company_name=?, updated_at=? WHERE id=?",
                    (company_name, now_iso(), session_id)
                )

            for data_type in ("dashboard", "roadmap", "document", "context"):
                if body.get(data_type):
                    _upsert_session_data(conn, session_id, data_type, body[data_type])

            log_action(conn, session_id, "generate_saved", f"Saved via {provider_name}")

        return jsonify({"ok": True, "session_id": session_id})

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Save failed: {str(e)}"}), 500

# ── Session management ────────────────────────────────────────────────────────

@app.route("/api/sessions", methods=["GET"])
def list_sessions():
    with get_db() as conn:
        rows = conn.execute(
            "SELECT id, company_name, url, provider, status, created_at, updated_at FROM sessions ORDER BY updated_at DESC"
        ).fetchall()
    return jsonify([dict(r) for r in rows])

@app.route("/api/session/<session_id>", methods=["GET"])
def load_session(session_id):
    with get_db() as conn:
        session = conn.execute("SELECT * FROM sessions WHERE id=?", (session_id,)).fetchone()
        if not session:
            return jsonify({"error": "Session not found"}), 404

        # Load latest version of each data type
        data_rows = conn.execute("""
            SELECT data_type, payload FROM session_data
            WHERE session_id=?
            AND version = (
                SELECT MAX(version) FROM session_data s2
                WHERE s2.session_id=session_data.session_id
                AND s2.data_type=session_data.data_type
            )
        """, (session_id,)).fetchall()

    result = dict(session)
    result["data"] = {}
    for row in data_rows:
        try:
            result["data"][row["data_type"]] = json.loads(row["payload"])
        except Exception:
            result["data"][row["data_type"]] = {}

    return jsonify(result)

@app.route("/api/session/<session_id>/save", methods=["POST"])
def save_session(session_id):
    """Save or update session data mid-wizard."""
    body = request.get_json(force=True)
    data_type = body.get("data_type")  # e.g. "scan", "wizard_state"
    payload = body.get("payload")

    if not data_type or payload is None:
        return jsonify({"error": "data_type and payload required"}), 400

    with get_db() as conn:
        session = conn.execute("SELECT id FROM sessions WHERE id=?", (session_id,)).fetchone()
        if not session:
            # Auto-create session
            conn.execute(
                "INSERT INTO sessions (id, company_name, url, provider, status, created_at, updated_at) VALUES (?,?,?,?,?,?,?)",
                (session_id, body.get("company_name", "Unknown"), body.get("url", ""), body.get("provider", ""), "draft", now_iso(), now_iso())
            )
        else:
            conn.execute("UPDATE sessions SET updated_at=? WHERE id=?", (now_iso(), session_id))

        _upsert_session_data(conn, session_id, data_type, payload)
        log_action(conn, session_id, f"save_{data_type}")

    return jsonify({"ok": True, "session_id": session_id})

@app.route("/api/session/<session_id>", methods=["DELETE"])
def delete_session(session_id):
    with get_db() as conn:
        conn.execute("DELETE FROM sessions WHERE id=?", (session_id,))
    return jsonify({"ok": True})

@app.route("/api/session/<session_id>/history", methods=["GET"])
def session_history(session_id):
    """Return all versions of strategy outputs for this session."""
    with get_db() as conn:
        rows = conn.execute(
            "SELECT data_type, version, created_at FROM session_data WHERE session_id=? ORDER BY data_type, version DESC",
            (session_id,)
        ).fetchall()
    return jsonify([dict(r) for r in rows])

# ── Helpers ───────────────────────────────────────────────────────────────────

def _upsert_session_data(conn, session_id: str, data_type: str, payload):
    """Insert new version or update if same version exists for this type."""
    existing = conn.execute(
        "SELECT MAX(version) as v FROM session_data WHERE session_id=? AND data_type=?",
        (session_id, data_type)
    ).fetchone()
    current_version = existing["v"] or 0

    # Check if content actually changed
    latest = conn.execute(
        "SELECT payload FROM session_data WHERE session_id=? AND data_type=? AND version=?",
        (session_id, data_type, current_version)
    ).fetchone()

    new_payload = json.dumps(payload, ensure_ascii=False)

    if latest and latest["payload"] == new_payload:
        return  # No change — don't create a new version

    new_version = current_version + 1
    conn.execute(
        "INSERT INTO session_data (id, session_id, data_type, version, payload, created_at) VALUES (?,?,?,?,?,?)",
        (str(uuid.uuid4()), session_id, data_type, new_version, new_payload, now_iso())
    )
    conn.execute("UPDATE sessions SET updated_at=? WHERE id=?", (now_iso(), session_id))


# ── Start ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    init_db()
    print(f"StratIQ running on http://localhost:{PORT}")
    app.run(host="0.0.0.0", port=PORT, debug=False)
