import pytest
from pages.home_page import HomePage


@pytest.fixture(scope="module")
def home(driver):
    return HomePage(driver)


@pytest.mark.regression
def test_home_is_loaded(home):
    """앱 실행 후 홈 화면(하단 탭바)이 표시되는지 확인"""
    assert home.is_loaded(), "홈 화면 하단 탭바가 보이지 않음"


@pytest.mark.regression
def test_home_has_products(home):
    """홈 화면에 상품 카테고리 탭(베스트 등)이 표시되는지 확인"""
    assert home.has_products(), "홈 화면에 상품 섹션 탭이 표시되지 않음"


@pytest.mark.regression
def test_home_scroll_down_and_back(home):
    """홈 화면에서 스크롤 후 다시 올라와도 하단 탭바가 유지되는지 확인"""
    home.scroll_down()
    home.scroll_down()
    home.scroll_up()
    assert home.is_loaded(), "스크롤 후 홈 화면 하단 탭바가 사라짐"


@pytest.mark.regression
def test_home_has_banner(home):
    """홈 화면 상단에 배너(ViewPager)가 표시되는지 확인"""
    assert home.has_banner(), "홈 화면에 배너가 표시되지 않음"


@pytest.mark.regression
@pytest.mark.image_validation
def test_home_no_broken_images(home):
    """홈 화면(배너·상품 이미지)에 깨진 이미지가 없는지 확인"""
    broken_images = home.find_broken_images()
    assert not broken_images, f"깨진 이미지 발견: {broken_images}"
