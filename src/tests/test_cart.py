import pytest


@pytest.mark.smoke
def test_cart_opens(home_page, cart_page):
    home_page.open_cart()
    assert cart_page.is_loaded(), "장바구니 화면이 열리지 않음"
