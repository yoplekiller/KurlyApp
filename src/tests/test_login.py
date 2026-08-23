import pytest
from config.test_data import TestData
from pages.login_page import LoginPage


@pytest.fixture(scope="module")
def login(driver):
    page = LoginPage(driver)
    page.navigate()
    return page


def test_login_screen_opens(login):
    """마이컬리 탭 진입 시 로그인 화면(아이디/비밀번호/로그인 버튼)이 표시되는지 확인"""
    assert login.is_loaded(), "마이컬리 탭에서 로그인 화면이 표시되지 않음"


@pytest.mark.skip(
    reason=(
        "실기기로 반복 검증하는 과정에서 확인됨: 짧은 시간에 같은 계정/기기로 잘못된 자격증명 로그인을 "
        "여러 번 시도하면 실제 운영 서버가 '아이디, 비밀번호를 확인해주세요' 알림을 더 이상 띄우지 않게 됨 "
        "(어뷰징 방지로 추정, 최초 1회 시도에서는 1초 내 정상 노출 확인됨). 운영 백엔드를 상대로 이 케이스를 "
        "반복 자동화하면 서버 상태에 따라 매번 다르게 실패하므로, 전용 테스트 계정/환경 없이는 이 테스트를 "
        "신뢰성 있게 자동화할 수 없음."
    )
)
def test_login_with_wrong_credentials(login):
    """잘못된 아이디/비밀번호로 로그인 시도 시 안내 알림이 뜨고, 확인 후 로그인 화면이 유지되는지 확인"""
    login.login(TestData.WRONG_USER_ID, TestData.WRONG_USER_PASSWORD)
    assert login.has_invalid_credentials_alert(), "잘못된 자격증명 안내 알림이 표시되지 않음"
    login.dismiss_alert()
    assert login.is_loaded(), "알림 확인 후 로그인 화면이 표시되지 않음"
