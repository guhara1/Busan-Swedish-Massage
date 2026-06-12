# 간다 GO — 부산 출장마사지·홈타이 안내 사이트

부산 전지역 방문 관리 안내를 위한 정적 사이트입니다.
Google SEO 가이드라인(도어웨이 방지, 중복·얇은 콘텐츠 방지, 키워드 반복 방지)을
구조적으로 강제하도록 설계되어 있습니다.

- 상호: 간다 GO
- 전화 예약: 0508-202-4719

## 빌드

의존성 없이 Python 3만 있으면 됩니다.

```bash
python3 build.py        # content/ → docs/ 생성 (sitemap.xml, robots.txt 포함)
python3 count.py content/regions/jung.html   # 단일 페이지 글자수 확인
```

로컬 미리보기:

```bash
python3 -m http.server -d docs 8000
```

## 배포 전 설정

`config.json`의 `site_url`을 실제 도메인으로 변경한 뒤 다시 빌드하세요.
canonical URL과 sitemap이 이 값을 기준으로 생성됩니다.

```json
{ "site_url": "https://실제도메인.com" }
```

GitHub Pages를 쓰는 경우 저장소 설정에서 `docs/` 폴더를 게시 대상으로 지정하면 됩니다.

## 구조

```
build.py          정적 사이트 생성기 (2,000자 미만 페이지 자동 noindex + sitemap 제외)
config.json       상호·전화·도메인·최소 글자수 설정
templates/        공통 레이아웃 (메뉴·푸터·CTA)
static/css/       스타일
content/          페이지 본문 (경로 = URL)
 ├ index.html         메인 (/)
 ├ busan.html         부산 출장마사지 종합 안내 (/busan/)
 ├ regions/           지역별 안내 (허브 + 16개 구·군 + 대표 동 상세)
 ├ stations/          지하철역별 안내 (허브 + 6개 노선 + 대표 역 상세)
 ├ themes/            테마별 안내 (허브 + 14개 테마)
 ├ courses.html       코스안내
 ├ booking.html       예약안내
 ├ guide.html         이용가이드
 ├ reviews.html       후기 (실후기 게시 전까지 noindex)
 └ support/           고객센터·개인정보처리방침·이용약관
docs/             빌드 결과물 (배포 대상)
```

## 콘텐츠 규칙

새 페이지를 추가하기 전에 반드시 [CONTENT_GUIDE.md](CONTENT_GUIDE.md)를 읽으세요.
핵심 규칙:

1. 인덱스 대상 페이지는 본문 2,000~2,500자(공백 포함) 고유 작성.
   미달 시 빌드가 자동으로 noindex 처리합니다.
2. 숫자 동·가(연산1~9동, 남포동1~6가 등)는 대표 동 페이지 1개로 통합.
3. 지역+역+테마 조합 페이지 금지 (예: "서면역 스웨디시" 페이지).
4. 지역명·역명만 바꾼 복붙 페이지 금지.
5. 환승역 페이지는 URL 1개로 통합.
6. 역·동 상세 페이지는 고유 콘텐츠를 쓸 수 있을 때만 추가
   (현재 대표 역 3곳, 대표 동 2곳 — 같은 기준으로 점진 확장).
7. 건전 방문 관리 서비스 기준으로만 작성. 불법·성매매 암시 문구 금지.

## 확장 방법 (역·동 페이지 추가)

1. `CONTENT_GUIDE.md`의 슬러그 표준 확인
2. `content/stations/<역slug>.html` 또는 `content/regions/<구slug>/<동slug>.html` 생성
3. 기존 상세 페이지(예: `content/stations/seomyeon.html`)를 형식 참고용으로만 사용
   — 문장 재사용 금지
4. `python3 count.py <파일>`로 글자수 확인 후 `python3 build.py`
5. 해당 노선 허브/구 페이지의 역·동 언급 부분에 링크 추가
