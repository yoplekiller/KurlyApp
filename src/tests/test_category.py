import pytest
from pages.category_page import CategoryPage


@pytest.fixture(scope="module")
def category(driver):
    page = CategoryPage(driver)
    page.navigate()
    return page


@pytest.mark.regression
def test_category_tab_opens(category):
    """카테고리 탭 진입 후 마켓컬리 탭 헤더가 표시되는지 확인"""
    assert category.is_loaded(), "카테고리 탭 헤더(마켓컬리)가 표시되지 않음"


@pytest.mark.regression
def test_category_list_visible(category):
    """카테고리 목록(채소 등)이 표시되는지 확인"""
    assert category.has_category_list(), "카테고리 사이드바 목록이 표시되지 않음"


@pytest.mark.regression
@pytest.mark.smoke
def test_beauty_kurly_tab_switch(category):
    """뷰티컬리 탭으로 전환되는지 확인"""
    category.switch_to_beauty()
    assert category.is_loaded(), "뷰티컬리 탭 전환 후 헤더가 사라짐"


@pytest.mark.regression
def test_category_item_opens_subcategory(category):
    """카테고리 사이드바 항목(채소)을 클릭하면 해당 하위 카테고리 화면으로 진입하는지 확인

    앞선 테스트가 뷰티컬리로 전환해뒀을 수 있어 category.navigate()로 마켓컬리 상태를
    다시 명시적으로 맞춘 뒤 진행한다.
    """
    category.navigate()
    category.open_first_category_item()
    assert category.is_on_category_detail(), "카테고리 항목 클릭 후 하위 카테고리 화면이 표시되지 않음"
