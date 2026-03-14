import os
import requests
from flask import Flask, send_file, request, jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

app = Flask(__name__)
CORS(app)

SCRAPE_TIMEOUT = 12
MAX_HTML_CHARS = 40000  # cap per page to keep Claude prompt size sane

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
}

def clean_html(html: str) -> str:
    """Strip scripts, styles, nav boilerplate — keep readable text content."""
    soup = BeautifulSoup(html, 'html.parser')
    for tag in soup(['script', 'style', 'noscript', 'iframe', 'svg', 'img',
                     'header', 'footer', 'nav', 'aside', 'form', 'button',
                     'meta', 'link', 'head']):
        tag.decompose()
    text = soup.get_text(separator='\n', strip=True)
    # Collapse excessive blank lines
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    return '\n'.join(lines)[:MAX_HTML_CHARS]

def safe_fetch(url: str) -> dict:
    try:
        r = requests.get(url, headers=HEADERS, timeout=SCRAPE_TIMEOUT, allow_redirects=True)
        r.raise_for_status()
        return {'url': url, 'status': 'ok', 'content': clean_html(r.text)}
    except requests.exceptions.SSLError:
        # Try without SSL verification as fallback
        try:
            r = requests.get(url, headers=HEADERS, timeout=SCRAPE_TIMEOUT,
                             allow_redirects=True, verify=False)
            return {'url': url, 'status': 'ok', 'content': clean_html(r.text)}
        except Exception as e:
            return {'url': url, 'status': 'error', 'content': '', 'error': str(e)}
    except Exception as e:
        return {'url': url, 'status': 'error', 'content': '', 'error': str(e)}

def build_candidate_urls(base_url: str) -> dict:
    """Given a base URL, build the 4 candidate page URLs to scrape."""
    parsed = urlparse(base_url)
    scheme = parsed.scheme or 'https'
    netloc = parsed.netloc or parsed.path  # handle bare domains like "company.com"
    if not netloc:
        netloc = base_url.replace('https://', '').replace('http://', '').split('/')[0]
    root = f"{scheme}://{netloc}"
    return {
        'homepage': root,
        'about':    root + '/about',
        'news':     root + '/news',
        'leadership': root + '/leadership',
    }

@app.route('/')
def index():
    html_path = os.path.join(os.path.dirname(__file__), 'stratiq_8.html')
    return send_file(html_path)

@app.route('/api/scrape', methods=['POST'])
def scrape():
    data = request.get_json(force=True)
    url = (data.get('url') or '').strip()
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    # Normalise URL
    if not url.startswith('http'):
        url = 'https://' + url

    pages = build_candidate_urls(url)
    results = {}
    for page_key, page_url in pages.items():
        results[page_key] = safe_fetch(page_url)

    return jsonify({
        'base_url': url,
        'pages': results
    })

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'version': '2.0'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=False)
