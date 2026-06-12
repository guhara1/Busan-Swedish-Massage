#!/usr/bin/env python3
"""단일 콘텐츠 파일의 본문 글자 수 확인: python3 count.py content/regions/jung.html"""
import sys
sys.path.insert(0, ".")
from build import parse_content, visible_char_count
from pathlib import Path

for arg in sys.argv[1:]:
    meta, body = parse_content(Path(arg))
    print(f"{arg}: {visible_char_count(body)}자")
