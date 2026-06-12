# 사이트 공통 설정
# 배포 도메인 확정 후 BASE_URL 을 실제 도메인으로 변경하세요.
BASE_URL = "https://busan-swedish-massage.pages.dev"

BRAND = "간다 GO"
PHONE = "0508-202-4719"
PHONE_DISPLAY = "0508-202-4719"

# IndexNow 인증 키 — 빌드 시 루트에 <키>.txt 파일이 생성되고,
# indexnow_ping.py 가 빙·네이버 등 IndexNow 참여 엔진에 색인을 통보할 때 사용한다.
# (키는 공개되어도 무방한 값이다 — 프로토콜 설계상 키 파일이 곧 소유 증명)
INDEXNOW_KEY = "5f5572fb1efd4e8e8e8c70f590d7fa52"

# 상단 메뉴 — 하위 메뉴에는 키워드를 반복하지 않고 지역명·역명만 표시한다.
NAV = [
    ("홈", "/", []),
    ("부산 출장마사지", "/busan/", [
        ("출장마사지 안내", "/busan/#service"),
        ("홈타이 안내", "/busan/#hometai"),
        ("전지역 방문 안내", "/busan/#coverage"),
        ("지하철역 인근 안내", "/busan/#stations"),
        ("예약 가능 시간", "/busan/#hours"),
        ("코스 선택 안내", "/busan/#course"),
        ("이용 전 확인사항", "/busan/#check"),
        ("위생·안전 안내", "/busan/#safety"),
        ("자주 묻는 질문", "/busan/#faq"),
    ]),
    ("지역별 안내", "/regions/", [
        ("부산 전체", "/regions/"),
        ("중구", "/regions/jung/"),
        ("서구", "/regions/seo/"),
        ("동구", "/regions/dong/"),
        ("영도구", "/regions/yeongdo/"),
        ("부산진구", "/regions/busanjin/"),
        ("동래구", "/regions/dongnae/"),
        ("남구", "/regions/nam/"),
        ("북구", "/regions/buk/"),
        ("해운대구", "/regions/haeundae/"),
        ("사하구", "/regions/saha/"),
        ("금정구", "/regions/geumjeong/"),
        ("강서구", "/regions/gangseo/"),
        ("연제구", "/regions/yeonje/"),
        ("수영구", "/regions/suyeong/"),
        ("사상구", "/regions/sasang/"),
        ("기장군", "/regions/gijang/"),
    ]),
    ("지하철역별 안내", "/stations/", [
        ("역 전체", "/stations/"),
        ("1호선", "/stations/line1/"),
        ("2호선", "/stations/line2/"),
        ("3호선", "/stations/line3/"),
        ("4호선", "/stations/line4/"),
        ("동해선 부산권", "/stations/donghae/"),
        ("부산김해경전철 부산권", "/stations/bgl/"),
        ("서면역", "/stations/seomyeon/"),
        ("해운대역", "/stations/haeundae/"),
        ("부산역", "/stations/busan-station/"),
    ]),
    ("테마별 안내", "/themes/", [
        ("전체 테마", "/themes/"),
        ("스웨디시", "/themes/swedish/"),
        ("로미로미", "/themes/lomilomi/"),
        ("타이마사지", "/themes/thai/"),
        ("중국마사지", "/themes/chinese/"),
        ("아로마테라피", "/themes/aroma/"),
        ("홈케어", "/themes/homecare/"),
        ("호텔식마사지", "/themes/hotel/"),
        ("발마사지", "/themes/foot/"),
        ("스포츠·경락", "/themes/sports/"),
        ("스킨케어", "/themes/skincare/"),
        ("왁싱", "/themes/waxing/"),
        ("커플 관리", "/themes/couple/"),
        ("24시간", "/themes/allnight/"),
        ("수면 가능", "/themes/sleep/"),
    ]),
    ("코스안내", "/courses/", [
        ("전체 코스", "/courses/"),
        ("피로 회복 관리", "/courses/#recovery"),
        ("아로마 관리", "/courses/#aroma"),
        ("스포츠 관리", "/courses/#sports"),
        ("홈타이 코스", "/courses/#hometai"),
        ("커플·가족 방문 관리", "/courses/#couple"),
        ("기업·단체 방문 관리", "/courses/#group"),
        ("가격 안내", "/courses/#price"),
        ("코스 선택 가이드", "/courses/#guide"),
    ]),
    ("예약안내", "/booking/", [
        ("예약 방법", "/booking/#how"),
        ("예약 가능 시간", "/booking/#hours"),
        ("방문 가능 장소", "/booking/#place"),
        ("결제 안내", "/booking/#payment"),
        ("변경·취소 안내", "/booking/#change"),
        ("예약 전 체크사항", "/booking/#check"),
    ]),
    ("이용가이드", "/guide/", [
        ("처음 이용하시는 분", "/guide/#first"),
        ("방문 전 준비사항", "/guide/#prepare"),
        ("위생 및 안전 기준", "/guide/#hygiene"),
        ("관리 후 주의사항", "/guide/#after"),
        ("금지행위 안내", "/guide/#prohibited"),
        ("이용 FAQ", "/guide/#faq"),
    ]),
    ("매거진", "/magazine/", [
        ("전체 글", "/magazine/"),
        ("마사지 비교 가이드", "/magazine/swedish-vs-thai/"),
        ("처음 이용 가이드", "/magazine/first-time-guide/"),
        ("수면과 마사지", "/magazine/sleep-and-massage/"),
        ("운동 후 회복", "/magazine/post-workout-timing/"),
        ("어깨·목 결림 관리", "/magazine/neck-shoulder-care/"),
        ("부모님 선물 가이드", "/magazine/parents-gift/"),
    ]),
    ("후기", "/reviews/", [
        ("전체 후기", "/reviews/"),
        ("후기 작성 안내", "/reviews/#write"),
    ]),
    ("고객센터", "/support/", [
        ("공지사항", "/support/#notice"),
        ("자주 묻는 질문", "/support/#faq"),
        ("1:1 문의", "/support/#contact"),
        ("제휴·기업 문의", "/support/#biz"),
        ("개인정보처리방침", "/support/privacy/"),
        ("이용약관", "/support/terms/"),
    ]),
]
