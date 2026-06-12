#!/usr/bin/env python3
"""META(title/h1/description) 도어웨이 패턴 검사.

지역·테마명(첫 토큰)을 마스킹한 뒤 동일 골격이 몇 번 반복되는지 집계한다.
사용: python3 meta_check.py            # 전체
      python3 meta_check.py regions/jung  # 특정 디렉터리/접두어만
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

prefix = sys.argv[1] if len(sys.argv) > 1 else ""
metas = []
for p in sorted(Path("content").rglob("*.html")):
    rel = str(p.relative_to("content"))
    if not rel.startswith(prefix):
        continue
    raw = p.read_text(encoding="utf-8")
    m = re.search(r"<!--META\s*(\{.*?\})\s*-->", raw, re.S)
    meta = json.loads(m.group(1))
    metas.append((rel, meta["title"], meta["description"], meta["h1"]))


def mask(s):
    return re.sub(r"^[^\s—|,·]+", "〈X〉", s)


print(f"검사 대상: {len(metas)}페이지\n")
problems = 0
for label, idx in [("타이틀", 1), ("H1", 3)]:
    c = Counter(mask(m[idx]) for m in metas)
    dups = [(s, n) for s, n in c.most_common() if n >= 3]
    print(f"=== {label} 골격 3회 이상 반복 ===")
    if dups:
        problems += 1
        for s, n in dups:
            print(f"{n:4d}  {s}")
    else:
        print("  없음 ✓")
    print()

c = Counter(mask(m[2])[:22] for m in metas)
dups = [(s, n) for s, n in c.most_common() if n >= 3]
print("=== 디스크립션 시작 골격(22자) 3회 이상 반복 ===")
if dups:
    problems += 1
    for s, n in dups:
        print(f"{n:4d}  {s}")
else:
    print("  없음 ✓")

# 길이 검사
print("\n=== 길이 이상 ===")
bad = False
for rel, t, d, h in metas:
    tl = len(t.replace(" | 간다 GO", ""))
    if not 12 <= tl <= 45:
        print(f"  타이틀 {tl}자: {rel} — {t}")
        bad = True
    if not 75 <= len(d) <= 165:
        print(f"  디스크립션 {len(d)}자: {rel}")
        bad = True
if not bad:
    print("  없음 ✓")
sys.exit(1 if problems else 0)
