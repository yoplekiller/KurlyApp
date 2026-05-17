import pytest


@pytest.mark.smoke
def test_home_loads(home_page):
    assert home_page.is_loaded(), "홈 화면이 로딩되지 않음"


@pytest.mark.smoke
def test_home_has_products(home_page):
    assert home_page.has_products(), "홈 화면에 상품 카드가 노출되지 않음"
