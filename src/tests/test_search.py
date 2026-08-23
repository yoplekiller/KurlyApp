import pytest
from pages.search_page import SearchPage


@pytest.fixture(scope="module")
def search(driver):
    page = SearchPage(driver)
    page.navigate()
    return page


def test_search_tab_opens(search):
    """검색 탭 진입 시 검색어 입력창이 표시되는지 확인"""
    assert search.is_loaded(), "검색 탭에서 검색어 입력창이 표시되지 않음"


def test_search_has_recommended_keywords(search):
    """검색 탭에 추천 검색어 섹션이 표시되는지 확인"""
    assert search.has_recommended_keywords(), "검색 탭에 추천 검색어 섹션이 표시되지 않음"
