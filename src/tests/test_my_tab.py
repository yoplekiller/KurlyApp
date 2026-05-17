import pytest


@pytest.mark.smoke
def test_my_tab_opens(home_page, my_tab_page):
    home_page.go_to_my_kurly()
    assert my_tab_page.is_loaded(), "마이탭이 열리지 않음"
    assert my_tab_page.requires_login() or my_tab_page.is_logged_in(), "마이탭 콘텐츠가 노출되지 않음"
