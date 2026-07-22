import pytest
from pytest_bdd import given, parsers, scenarios, then, when

scenarios("features/search.feature")


@given("마켓컬리 앱이 실행되어 있다")
def app_launched(driver):
    pass


@given("검색 탭에 진입해 있다", target_fixture="opened_search_page")
def search_already_open(search_page):
    search_page.navigate()
    return search_page


@when("검색 탭으로 이동한다")
def navigate_to_search(search_page):
    search_page.navigate()


@when(parsers.parse('검색창에 "{keyword}"를 입력한다'))
def input_keyword(opened_search_page, keyword):
    opened_search_page.input_text_to_search(keyword)


@when("검색을 실행한다")
def execute_search(opened_search_page):
    opened_search_page.submit_search()


@then("검색창이 표시된다")
def check_search_input(search_page):
    assert search_page.is_loaded(), "검색창이 표시되지 않음"


@then(parsers.parse('"{keyword}" 검색 결과가 표시된다'))
def check_search_results(opened_search_page, keyword):
    assert opened_search_page.has_results(keyword), f'"{keyword}" 검색 결과가 표시되지 않음'
