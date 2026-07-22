import pytest
from pages.category_page import CategoryPage


@pytest.fixture(scope="module")
def category(driver):
    page = CategoryPage(driver)
    page.navigate()
    return page


def test_category_tab_opens(category):
    """카테고리 탭 진입 후 마켓컬리 탭 헤더가 표시되는지 확인"""
    assert category.is_loaded(), "카테고리 탭 헤더(마켓컬리)가 표시되지 않음"


def test_category_list_visible(category):
    """카테고리 목록(채소 등)이 표시되는지 확인"""
    assert category.has_category_list(), "카테고리 사이드바 목록이 표시되지 않음"


def test_beauty_kurly_tab_switch(category):
    """뷰티컬리 탭으로 전환되는지 확인"""
    category.switch_to_beauty()
    assert category.is_loaded(), "뷰티컬리 탭 전환 후 헤더가 사라짐"
