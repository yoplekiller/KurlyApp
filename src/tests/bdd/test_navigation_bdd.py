import pytest
from pytest_bdd import given, scenarios, then, when

from pages.category_page import CategoryPage
from utils.popup_handler import handle_kurly_popups

scenarios("features/navigation.feature")


@given("마켓컬리 앱이 실행되어 있다")
def app_launched(driver):
    pass


@given("카테고리 탭에 진입해 있다", target_fixture="nav_category_page")
def category_opened(category_page):
    category_page.navigate()
    return category_page


@given("검색 탭에 진입해 있다", target_fixture="nav_search_page")
def search_opened(search_page):
    search_page.navigate()
    return search_page


@when("홈 탭으로 이동한다")
def go_home(home_page):
    home_page.navigate()


@when("카테고리 탭으로 이동한다")
def go_category(nav_search_page, driver):
    CategoryPage(driver).navigate()
    handle_kurly_popups(driver, wait_time=3)


@then("하단 탭바가 표시된다")
def check_bottom_nav(home_page):
    assert home_page.is_loaded(), "하단 탭바가 보이지 않음"


@then("상품 섹션 탭이 표시된다")
def check_products(home_page):
    assert home_page.has_products(), "상품 섹션 탭이 표시되지 않음"


@then("마켓컬리 탭 헤더가 표시된다")
def check_market_kurly_header(category_page):
    assert category_page.is_loaded(), "마켓컬리 탭 헤더가 표시되지 않음"
