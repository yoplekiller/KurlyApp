import pytest
from pages.lounge_page import LoungePage


@pytest.fixture(scope="module")
def lounge(driver):
    page = LoungePage(driver)
    page.navigate()
    return page


@pytest.mark.smoke
def test_lounge_tab_opens(lounge):
    """라운지 탭 진입 시 라운지 화면이 표시되는지 확인"""
    assert lounge.is_loaded(), "라운지 탭에서 라운지 화면이 표시되지 않음"


def test_lounge_has_content_tabs(lounge):
    """라운지 화면에 콘텐츠 탭(전체 콘텐츠 등)이 표시되는지 확인"""
    assert lounge.has_content_tabs(), "라운지 화면에 콘텐츠 탭이 표시되지 않음"
