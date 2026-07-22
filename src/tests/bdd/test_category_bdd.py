import pytest
from pytest_bdd import given, scenarios, then, when
from config.app_config import AppConfig
from utils.popup_handler import handle_kurly_popups

scenarios("features/category.feature")


@given("마켓컬리 앱이 실행되어 있다")
def app_launched(driver):
    pass


@given("카테고리 탭에 진입해 있다", target_fixture="navigated_category_page")
def category_already_open(category_page):
    category_page.navigate()
    return category_page


@when("카테고리 탭으로 이동한다")
def navigate_to_category(category_page, driver):
    category_page.navigate()
    handle_kurly_popups(driver, wait_time=3)


@when("뷰티컬리 탭을 선택한다")
def select_beauty_tab(navigated_category_page):
    navigated_category_page.switch_to_beauty()


@then("마켓컬리 탭 헤더가 표시된다")
def check_market_kurly_header(category_page):
    assert category_page.is_loaded(), "마켓컬리 탭 헤더가 표시되지 않음"


@then("뷰티컬리 탭 메뉴가 표시된다")
def check_beauty_tab_visible(category_page):
    assert category_page.has_beauty_tab(), "뷰티컬리 탭 메뉴가 표시되지 않음"


@then("카테고리 탭 헤더가 표시된다")
def check_header_after_switch(navigated_category_page):
    assert navigated_category_page.is_loaded(), "뷰티컬리 탭 전환 후 헤더가 사라짐"
