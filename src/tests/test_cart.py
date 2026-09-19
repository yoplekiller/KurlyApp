import pytest
from pages.cart_page import CartPage
from pages.home_page import HomePage


@pytest.fixture(scope="module")
def cart(driver):
    HomePage(driver).navigate()
    page = CartPage(driver)
    page.open_from_home()
    return page


@pytest.mark.regression
@pytest.mark.smoke
def test_cart_opens(cart):
    """홈 화면 우측 상단 아이콘으로 장바구니 화면이 열리는지 확인"""
    assert cart.is_loaded(), "장바구니 화면이 열리지 않음"


@pytest.mark.regression
def test_cart_can_close(cart):
    """장바구니 화면을 닫으면 화면이 사라지는지 확인"""
    cart.close()
    assert not cart.is_loaded(timeout=3), "장바구니 화면을 닫았는데도 여전히 표시됨"


@pytest.mark.regression
@pytest.mark.smoke
def test_quick_add_to_cart_increases_badge_count(driver):
    """목록에서 퀵 담기로 상품을 담으면 담기 확인 메시지가 뜨고, 장바구니 배지 수량이 유지되거나 늘어나는지 확인.

    장바구니 화면 내부(담긴 상품 목록)는 WebView로 렌더링되고 원격 디버깅이 꺼져 있어
    Appium으로 접근할 수 없다(실기기 조사로 확인) - 그래서 담기 성공 여부는 1차로 크로스셀
    시트의 네이티브 확인 메시지("장바구니에 상품을 담았어요.")로 검증한다. 배지 숫자는 "고유
    상품 개수"로 보이며(실기기 조사로 확인) 이미 장바구니에 있는 상품을 다시 담으면 수량만
    올라가고 배지는 그대로일 수 있어 - 정확히 +1이 아니라 "줄어들지는 않는지"까지만 보조로 확인한다.
    """
    home = HomePage(driver)
    home.navigate()
    home.open_best_products()
    cart = CartPage(driver)
    before = cart.get_badge_count()

    confirmed = home.quick_add_first_product_to_cart()

    assert confirmed, "퀵 담기 후 장바구니 담기 확인 메시지가 표시되지 않음"
    after = cart.get_badge_count()
    assert after >= before, f"퀵 담기 후 장바구니 배지가 {before}->{after}로 오히려 줄어듦"
