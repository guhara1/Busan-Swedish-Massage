# 전체 페이지 목록 집계
from . import about, magazine, main
from .loader import load_dir, load_page

PAGES = (
    [main.PAGE]
    + [load_page("busan.html")]
    + load_dir("regions", with_pricing=True)
    + load_dir("stations", with_pricing=True)
    + load_dir("themes")
    + [
        load_page("courses.html"),
        load_page("booking.html"),
        load_page("guide.html"),
        load_page("reviews.html"),
    ]
    + load_dir("support")
    + magazine.PAGES
    + [about.PAGE]
)
