import pytest
from pytest_bdd import given, parsers, scenarios, then, when

scenarios("features/home.feature")


@given("마켓컬리 앱이 실행되어 있다")
def app_launched(driver):
    pass


@when("홈 화면에 진입한다")
def navigate_home(home_page):
    pass  # 앱 시작 시 홈 화면이 기본값


@when("홈 화면에서 아래로 스크롤한다")
def scroll_down(home_page):
    home_page.scroll_down()
    home_page.scroll_down()


@when("홈 화면에서 위로 스크롤한다")
def scroll_up(home_page):
    home_page.scroll_up()


@then("하단 탭바가 표시된다")
def check_bottom_nav(home_page):
    assert home_page.is_loaded(), "하단 탭바가 보이지 않음"


@then("상품 섹션 탭이 표시된다")
def check_products(home_page):
    assert home_page.has_products(), "상품 섹션 탭이 표시되지 않음"


@then("상단 배너가 표시된다")
def check_banner(home_page):
    assert home_page.has_banner(), "상단 배너가 표시되지 않음"


@then(parsers.parse("홈 화면에 {element} 노출"))
def check_home_element(home_page, element):
    checks = {
        "하단 탭바": home_page.is_loaded,
        "상품 섹션 탭": home_page.has_products,
        "상단 배너": home_page.has_banner,
    }
    checker = checks.get(element.strip())
    assert checker is not None, f"알 수 없는 요소: {element}"
    assert checker(), f"{element}가 표시되지 않음"
