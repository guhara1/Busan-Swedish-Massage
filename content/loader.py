# 레거시 HTML 조각(content/**/*.html)을 템플릿 페이지 dict로 변환하는 로더.
#
# 콘텐츠 파일 형식:
#   <!--META { "title": ..., "description": ..., "h1": ..., "crumbs": [...] } -->
#   <p>본문 ...</p>  (h2 단위 섹션)
#
# 변환 규칙:
#   - 첫 <p> → <p class="lead">
#   - <h2> 블록 → <section id=...><h2>...</h2>...</section> (TOC·앵커용)
#   - <dl class="faq"><dt>Q. x</dt><dd>A. y</dd></dl> → <div class="faq-item"><h3>x</h3><p>y</p></div>
#   - 지역·역 페이지에는 공용 요금 블록(PRICING)을, 모든 페이지에 CTA를 덧붙인다.
import json
import re
from pathlib import Path

from .pricing import PRICING
from .site import PHONE, PHONE_DISPLAY

CONTENT_DIR = Path(__file__).parent
META_RE = re.compile(r"<!--META\s*(\{.*?\})\s*-->", re.DOTALL)

CTA = f"""
<section class="cta">
<h2>예약문의</h2>
<p>방문 위치와 희망 시간을 알려주시면 가능 여부를 바로 확인해 드립니다.</p>
<a class="cta-phone" href="tel:{PHONE}">{PHONE_DISPLAY}</a>
</section>
"""

# 상단 메뉴 하위 앵커와 일치해야 하는 섹션 id (h2 텍스트 → id)
ANCHORS = {
    "index.html": {
        "부산 출장마사지·홈타이 서비스 안내": "service",
        "부산 전지역 방문 가능 안내": "coverage",
        "구·군별 지역 안내": "areas",
        "대표 동·읍·면 안내": "dong",
        "지하철역 인근 안내": "stations",
        "테마별 관리 안내": "themes",
        "코스 선택 안내": "course",
        "예약 진행 방식": "booking",
        "이용 전 확인사항": "check",
        "위생 및 안전 안내": "safety",
        "자주 묻는 질문": "faq",
    },
    "busan.html": {
        "부산 출장마사지 안내": "service",
        "부산 홈타이 안내": "hometai",
        "부산 전지역 방문 가능 안내": "coverage",
        "부산 지하철역 인근 안내": "stations",
        "예약 가능 시간": "hours",
        "코스 선택 안내": "course",
        "이용 전 확인사항": "check",
        "위생 및 안전 안내": "safety",
        "자주 묻는 질문": "faq",
    },
    "courses.html": {
        "피로 회복 관리": "recovery",
        "아로마 관리": "aroma",
        "스포츠 관리": "sports",
        "홈타이 코스": "hometai",
        "커플·가족 방문 관리": "couple",
        "기업·단체 방문 관리": "group",
        "가격 안내": "price",
        "코스 선택 가이드": "guide",
        "자주 묻는 질문": "faq",
    },
    "booking.html": {
        "예약 방법": "how",
        "예약 가능 시간": "hours",
        "방문 가능 장소": "place",
        "결제 안내": "payment",
        "변경·취소 안내": "change",
        "예약 전 체크사항": "check",
        "자주 묻는 질문": "faq",
    },
    "guide.html": {
        "처음 이용하시는 분": "first",
        "방문 전 준비사항": "prepare",
        "위생 및 안전 기준": "hygiene",
        "관리 후 주의사항": "after",
        "금지행위 안내": "prohibited",
        "이용 FAQ": "faq",
    },
    "reviews.html": {
        "후기 안내": "about",
        "후기 작성 안내": "write",
        "문의": "contact",
    },
    "support/index.html": {
        "공지사항": "notice",
        "자주 묻는 질문": "faq",
        "1:1 문의": "contact",
        "제휴·기업 문의": "biz",
        "약관·정책": "policy",
    },
}


def _convert_faq(html: str) -> str:
    def repl(m):
        inner = m.group(1)
        items = re.findall(r"<dt>\s*(?:Q\.\s*)?(.*?)</dt>\s*<dd>\s*(?:A\.\s*)?(.*?)</dd>", inner, re.S)
        return "".join(
            f'<div class="faq-item">\n<h3>{q.strip()}</h3>\n<p>{a.strip()}</p>\n</div>\n'
            for q, a in items
        )

    return re.sub(r'<dl class="faq">(.*?)</dl>', repl, html, flags=re.S)


def _sectionize(body: str, anchors: dict) -> str:
    """h2 단위로 <section> 래핑. 첫 단락에 lead 클래스를 부여한다."""
    parts = re.split(r"(?=<h2>)", body)
    intro = parts[0].strip()
    if intro:
        intro = re.sub(r"^<p>", '<p class="lead">', intro, count=1)

    sections = []
    for chunk in parts[1:]:
        m = re.match(r"<h2>(.*?)</h2>(.*)", chunk, re.S)
        title, rest = m.group(1).strip(), m.group(2).strip()
        plain = re.sub(r"<[^>]+>", "", title).strip()
        sid = anchors.get(plain)
        id_attr = f' id="{sid}"' if sid else ""
        sections.append(f"<section{id_attr}>\n<h2>{title}</h2>\n{rest}\n</section>")

    return (intro + "\n\n" if intro else "") + "\n\n".join(sections)


def _url_path(rel: str) -> str:
    rel = rel[:-len(".html")]
    if rel == "index":
        return ""
    if rel.endswith("/index"):
        rel = rel[:-len("/index")]
    return rel + "/"


def load_page(rel: str, with_pricing: bool = False) -> dict:
    """content/ 기준 상대 경로의 HTML 조각을 페이지 dict로 변환한다."""
    raw = (CONTENT_DIR / rel).read_text(encoding="utf-8")
    m = META_RE.search(raw)
    if not m:
        raise ValueError(f"META 블록이 없습니다: {rel}")
    meta = json.loads(m.group(1))
    body = raw[m.end():].strip()

    body = _convert_faq(body)
    body = _sectionize(body, ANCHORS.get(rel, {}))
    if with_pricing:
        body += PRICING
    body += CTA

    crumbs = [tuple(c) for c in meta.get("crumbs", [])]
    crumbs.append((meta["h1"], None))

    extra_head = ""
    if meta.get("jsonld"):
        extra_head = ('<script type="application/ld+json">'
                      + json.dumps(meta["jsonld"], ensure_ascii=False)
                      + "</script>")

    page = {
        "path": _url_path(rel),
        "title": meta["title"],
        "desc": meta["description"],
        "h1": meta["h1"],
        "body": body,
        "breadcrumb": crumbs,
    }
    if extra_head:
        page["extra_head"] = extra_head
    if meta.get("noindex"):
        page["noindex"] = True
    return page


def load_dir(subdir: str, with_pricing: bool = False) -> list:
    """하위 디렉터리의 모든 HTML 조각을 변환한다 (허브 index.html 우선)."""
    base = CONTENT_DIR / subdir
    files = sorted(base.rglob("*.html"), key=lambda p: (p.name != "index.html", str(p)))
    return [
        load_page(str(p.relative_to(CONTENT_DIR)), with_pricing=with_pricing)
        for p in files
    ]
