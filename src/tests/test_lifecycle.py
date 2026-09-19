import pytest

from pages.home_page import HomePage


@pytest.mark.regression
@pytest.mark.smoke
def test_resumes_correctly_after_backgrounding(driver):
    """앱을 백그라운드로 보냈다가 복귀했을 때 화면 상태가 유지되는지 확인"""
    home = HomePage(driver)
    home.navigate()
    assert home.is_loaded(), "백그라운드 전환 전 홈 화면이 로드되지 않음"

    driver.background_app(3)  # 3초간 백그라운드로 전환 후 자동 복귀

    assert home.is_loaded(), "백그라운드에서 복귀한 후 홈 화면이 정상적으로 표시되지 않음"
    assert home.has_products(), "백그라운드에서 복귀한 후 상품 목록이 사라짐"
