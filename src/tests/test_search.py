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


@pytest.mark.smoke
def test_search_returns_results(search):
    """검색어 입력 후 제출하면 결과 화면에 해당 키워드가 노출되는지 확인"""
    search.input_text_to_search("샴푸")
    search.submit_search()
    assert search.has_results("샴푸"), "검색 실행 후 결과 화면에 검색어 관련 콘텐츠가 표시되지 않음"
