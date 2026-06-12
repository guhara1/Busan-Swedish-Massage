# 간다 GO — 부산 출장마사지·홈타이 안내 사이트

부산 전지역 방문 관리(출장마사지·홈타이) 안내용 정적 사이트입니다.
예약전화: **0508-202-4719**

## 구조

- 정적 HTML 사이트 — 어느 호스팅(GitHub Pages, Netlify, 일반 웹서버)에서든 그대로 서빙 가능
- `build.py` + `content/` 패키지에서 페이지를 생성하는 빌드 방식
- 생성물(각 디렉터리의 `index.html`, `sitemap.xml`, `robots.txt`, `404.html`)도 저장소에 포함

```
build.py            # 빌드 스크립트 (레이아웃·글자수 검사·sitemap 생성)
make_icons.py       # 파비콘·OG 이미지 생성 (1회성, Pillow 필요)
content/
  site.py           # 상호·전화·BASE_URL·메뉴 구조
  main.py           # 메인 페이지 (히어로 + LocalBusiness/FAQPage JSON-LD)
  loader.py         # HTML 조각 → 페이지 변환 (섹션 래핑·FAQ·요금 블록·CTA)
  pricing.py        # 공용 요금 블록
  magazine.py       # 매거진 허브 + 아티클 6편
  about.py          # 운영자 소개 (E-E-A-T)
  *.html, */*.html  # 페이지 본문 (메인·부산 안내·지역·역·테마·코스·예약·가이드 등)
assets/             # CSS, 모바일 내비 JS, 파비콘, OG 이미지
```

## 빌드

```bash
python3 build.py
```

빌드 시 페이지별 본문 글자수 리포트가 출력됩니다.

## SEO 운영 원칙 (빌드에 강제됨)

- 본문 **2,000자 미만 페이지는 자동 `noindex`** 처리되고 sitemap에서 제외
- 지역은 16개 구·군 + 고유 콘텐츠가 준비된 대표 동만 — 숫자 동·가 페이지 없음
  (연산1~9동 → 연산동, 남포동1~6가 → 남포동 통합)
- 역은 노선 허브 6개 + 대표 역 상세 — 환승역도 URL 하나, 출구별 페이지 없음
- **지역+역+테마 조합 페이지 없음** (도어웨이 방지) — 테마는 독립 페이지로만 운영
- 상단/하위 메뉴와 푸터에 키워드·지역명·역명 대량 나열 없음
- 모든 페이지 본문은 페이지별 고유 작성 (지역명만 바꾼 복붙 없음)

자세한 작성 규칙과 슬러그 표준은 [CONTENT_GUIDE.md](CONTENT_GUIDE.md) 참고.

## 배포·색인 (도메인: busan-swedish-massage.pages.dev)

`BASE_URL`은 `content/site.py`에 설정되어 있고, 빌드 시 canonical·sitemap.xml·
rss.xml·robots.txt·IndexNow 키 파일에 자동 반영된다.

### 색인 자동화 (이미 구성됨)

- **sitemap.xml** — 인덱스 189페이지 + `lastmod`(빌드 날짜)
- **rss.xml** — 매거진 아티클 피드 (네이버 서치어드바이저 RSS 제출용)
- **robots.txt** — 전체 허용 + Yeti(네이버)·Googlebot 명시 + Sitemap 위치
- **IndexNow** — 키 파일(`<키>.txt`) 배포 + `indexnow_ping.py`
  - 글 올린 뒤: `python3 indexnow_ping.py /magazine/new-post/` (빙·네이버 즉시 통보)
  - 전체 재통보: `python3 indexnow_ping.py --all`
  - GitHub Actions(`.github/workflows/indexnow.yml`)가 main 푸시 시 자동 실행
- **구글** — IndexNow 미참여. `google_indexing.py`(Indexing API, 정책 제한 주의)
  포함. sitemap ping 엔드포인트는 2024년 폐기되어 사용하지 않는다.

### 최초 1회 수동 등록 (가장 효과 큼)

1. **구글 서치콘솔**: 속성 등록 → `sitemap.xml` 제출 → 메인 URL 검사 → 색인 요청
2. **네이버 서치어드바이저**: 사이트 등록(인증 태그 이미 삽입됨) →
   요청 &gt; 사이트맵 제출(`sitemap.xml`) + RSS 제출(`rss.xml`) →
   웹 페이지 수집 요청으로 메인·허브 URL 수동 수집
