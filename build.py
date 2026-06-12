#!/usr/bin/env python3
"""간다 GO — 부산 출장마사지·홈타이 정적 사이트 생성기.

content/ 아래의 HTML 조각 파일을 templates/base.html에 결합해 docs/로 출력한다.

규칙(자동 적용):
- 본문 텍스트(공백 제외)가 2,000자 미만인 페이지는 noindex 처리하고 sitemap에서 제외한다.
- META 주석의 "noindex": true 로 강제 noindex 가능(후기·약관 등).
- sitemap.xml, robots.txt 자동 생성.

콘텐츠 파일 형식:
    <!--META
    { "title": "...", "description": "...", "h1": "...", "crumbs": [["지역별 안내","/regions/"]] }
    -->
    <p>본문 ...</p>

경로 매핑: content/regions/jung.html → docs/regions/jung/index.html (URL /regions/jung/)
           content/regions/index.html → docs/regions/index.html (URL /regions/)
"""

import json
import re
import shutil
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).parent
CONTENT = ROOT / "content"
TEMPLATES = ROOT / "templates"
STATIC = ROOT / "static"
OUT = ROOT / "docs"

CONFIG = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
SITE_URL = CONFIG["site_url"].rstrip("/")
MIN_CHARS = CONFIG.get("min_index_chars", 2000)

META_RE = re.compile(r"<!--META\s*(\{.*?\})\s*-->", re.DOTALL)


class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.chunks = []

    def handle_data(self, data):
        self.chunks.append(data)


def visible_char_count(html: str) -> int:
    """태그를 제외한 본문 글자 수(공백 포함, 연속 공백은 1자로 정규화)."""
    p = TextExtractor()
    p.feed(html)
    text = "".join(p.chunks)
    return len(re.sub(r"\s+", " ", text).strip())


def parse_content(path: Path):
    raw = path.read_text(encoding="utf-8")
    m = META_RE.search(raw)
    if not m:
        sys.exit(f"META 블록이 없습니다: {path}")
    meta = json.loads(m.group(1))
    body = raw[m.end():].strip()
    return meta, body


def url_for(path: Path) -> str:
    rel = path.relative_to(CONTENT).with_suffix("")
    if rel.name == "index":
        rel = rel.parent
    url = "/" + str(rel).replace("\\", "/").strip("./")
    if url == "/.":
        url = "/"
    if not url.endswith("/"):
        url += "/"
    return url.replace("//", "/")


def breadcrumb_html(meta, url):
    crumbs = [["홈", "/"]] + meta.get("crumbs", [])
    if url == "/":
        return ""
    items = "".join(
        f'<li><a href="{href}">{label}</a></li>' for label, href in crumbs
    )
    items += f"<li aria-current=\"page\">{meta['h1']}</li>"
    return f'<nav class="breadcrumb" aria-label="현재 위치"><ol>{items}</ol></nav>'


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    base = (TEMPLATES / "base.html").read_text(encoding="utf-8")
    pages = []
    warnings = []

    for path in sorted(CONTENT.rglob("*.html")):
        meta, body = parse_content(path)
        url = url_for(path)
        chars = visible_char_count(body)
        noindex = meta.get("noindex", False) or chars < MIN_CHARS
        if noindex and not meta.get("noindex", False):
            warnings.append(f"  [noindex 자동 적용] {url} — 본문 {chars}자 (< {MIN_CHARS})")

        robots = '<meta name="robots" content="noindex, follow">' if noindex else ""
        jsonld = ""
        if meta.get("jsonld"):
            jsonld = ('<script type="application/ld+json">'
                      + json.dumps(meta["jsonld"], ensure_ascii=False)
                      + "</script>")

        html = base
        for key, value in {
            "{{TITLE}}": meta["title"],
            "{{DESCRIPTION}}": meta["description"],
            "{{CANONICAL}}": SITE_URL + url,
            "{{ROBOTS}}": robots,
            "{{JSONLD}}": jsonld,
            "{{H1}}": meta["h1"],
            "{{BREADCRUMB}}": breadcrumb_html(meta, url),
            "{{BODY}}": body,
            "{{PHONE}}": CONFIG["phone"],
            "{{PHONE_TEL}}": CONFIG["phone"].replace("-", ""),
            "{{BRAND}}": CONFIG["brand"],
        }.items():
            html = html.replace(key, value)

        out_path = OUT / url.strip("/") / "index.html" if url != "/" else OUT / "index.html"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(html, encoding="utf-8")
        pages.append((url, chars, noindex))

    # 정적 파일 복사
    if STATIC.exists():
        shutil.copytree(STATIC, OUT, dirs_exist_ok=True)

    # sitemap.xml — 인덱스 허용 페이지만 포함
    urls = "\n".join(
        f"  <url><loc>{SITE_URL}{u}</loc></url>" for u, _, ni in pages if not ni
    )
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}\n</urlset>\n",
        encoding="utf-8",
    )
    (OUT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n",
        encoding="utf-8",
    )

    indexed = sum(1 for _, _, ni in pages if not ni)
    print(f"빌드 완료: 전체 {len(pages)}페이지 (인덱스 {indexed} / noindex {len(pages) - indexed})")
    for w in warnings:
        print(w)
    print("\nURL                                          글자수   인덱스")
    for u, c, ni in pages:
        print(f"{u:<44} {c:>6}   {'noindex' if ni else 'index'}")


if __name__ == "__main__":
    build()
