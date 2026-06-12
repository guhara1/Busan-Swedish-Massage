#!/usr/bin/env python3
"""콘텐츠 파일의 최종 본문 글자수 확인 (CTA 포함, 요금 블록 제외 — 빌드와 동일 기준).

사용: python3 count.py regions/haeundae/u-dong.html  (content/ 기준 상대 경로)
"""
import sys

sys.path.insert(0, ".")
from build import text_length
from content.loader import load_page

for rel in sys.argv[1:]:
    page = load_page(rel, with_pricing=rel.startswith(("regions/", "stations/")))
    print(f"{rel}: {text_length(page['body'])}자")
