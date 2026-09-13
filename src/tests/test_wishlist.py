import pytest
from pages.home_page import HomePage
from pages.product_detail_page import ProductDetailPage


@pytest.fixture(scope="module")
def product_detail(driver):
    home = HomePage(driver)
    home.navigate()
    home.open_best_products()
    home.open_first_product()
    return ProductDetailPage(driver)


@pytest.mark.smoke
def test_wishlist_requires_login(product_detail):
    """비로그인 상태에서 찜(픽) 버튼을 누르면 로그인 유도 안내가 표시되는지 확인"""
    product_detail.tap_pick_button()
    assert product_detail.has_login_prompt(), "찜 버튼 클릭 시 로그인 유도 안내가 표시되지 않음"


def test_wishlist_prompt_can_cancel(product_detail):
    """로그인 유도 안내를 취소하면 안내가 사라지는지 확인"""
    product_detail.cancel_login_prompt()
    assert not product_detail.has_login_prompt(timeout=3), "안내를 취소했는데도 여전히 표시됨"
