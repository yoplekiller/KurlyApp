import pytest
from config.test_data import TestData


@pytest.mark.smoke
def test_search_returns_results(home_page, search_page):
    """정상 키워드 검색 시 상품이 노출되는지 확인"""
    home_page.go_to_search()
    search_page.search(TestData.SEARCH_KEYWORD)
    assert search_page.has_results(), f"'{TestData.SEARCH_KEYWORD}' 검색 결과가 없음"


@pytest.mark.regression
def test_search_with_no_result_keyword(home_page, search_page):
    """결과 없는 키워드 검색 시 결과 없음 화면이 노출되는지 확인"""
    home_page.go_to_search()
    search_page.search(TestData.NO_RESULT_KEYWORD)
    assert search_page.is_no_result(), "결과 없음 화면이 노출되지 않음"
