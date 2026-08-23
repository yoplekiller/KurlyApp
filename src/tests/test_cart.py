import pytest
from pages.cart_page import CartPage
from pages.home_page import HomePage


@pytest.fixture(scope="module")
def cart(driver):
    HomePage(driver).navigate()
    page = CartPage(driver)
    page.open_from_home()
    return page


@pytest.mark.smoke
def test_cart_opens(cart):
    """홈 화면 우측 상단 아이콘으로 장바구니 화면이 열리는지 확인"""
    assert cart.is_loaded(), "장바구니 화면이 열리지 않음"


def test_cart_can_close(cart):
    """장바구니 화면을 닫으면 화면이 사라지는지 확인"""
    cart.close()
    assert not cart.is_loaded(timeout=3), "장바구니 화면을 닫았는데도 여전히 표시됨"
