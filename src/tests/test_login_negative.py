import pytest


# 로그인 실패 시 로그인 화면이 유지되는지 검증하는 테스트
@pytest.mark.flaky(reruns=1)
def test_login_with_wrong_credentials(home_page, my_tab_page, login_page, wrong_user_credentials):
    home_page.go_to_my_kurly()
    my_tab_page.go_to_login()
    login_page.login(
        wrong_user_credentials["user_id"] or "wrong@example.com",
        wrong_user_credentials["password"] or "wrong-password",
    )
    assert login_page.is_login_screen()
