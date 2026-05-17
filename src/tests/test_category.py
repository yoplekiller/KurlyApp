import pytest


@pytest.mark.smoke
def test_category_tab(home_page, category_page):
    home_page.go_to_category()
    assert category_page.has_categories(), "카테고리 탭이 열리지 않거나 카테고리 목록이 없음"
