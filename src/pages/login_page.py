from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver

from config.app_config import AppConfig
from pages.base_page import BasePage

_MY_TAB = (AppiumBy.ID, "com.dbs.kurly.m2:id/mykurly")
_EMAIL_INPUT = (AppiumBy.ID, "com.dbs.kurly.m2:id/etId")
_PASSWORD_INPUT = (AppiumBy.ID, "com.dbs.kurly.m2:id/etPassword")
_LOGIN_BUTTON = (AppiumBy.ID, "com.dbs.kurly.m2:id/loginButton")
_INVALID_CREDENTIALS_ALERT = (AppiumBy.XPATH, "//*[@text='아이디, 비밀번호를 확인해주세요.']")
_ALERT_CONFIRM_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("확인")')


class LoginPage(BasePage):
    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

    def navigate(self) -> None:
        # 마이컬리 탭은 로그인 상태가 아니면 곧바로 로그인 화면을 보여준다(별도 진입 버튼 없음).
        self.click(_MY_TAB)

    def is_loaded(self, timeout: int = AppConfig.DEFAULT_TIMEOUT) -> bool:
        return self.is_visible(_LOGIN_BUTTON, timeout)

    def login(self, user_id: str, password: str) -> None:
        self.input_text(_EMAIL_INPUT, user_id)
        self.input_text(_PASSWORD_INPUT, password)
        self.click(_LOGIN_BUTTON)

    def has_invalid_credentials_alert(self, timeout: int = AppConfig.LONG_TIMEOUT) -> bool:
        # 실제 로그인 API 응답을 기다려야 알림이 뜨므로 네트워크 지연을 감안해 넉넉히 대기한다.
        return self.is_visible(_INVALID_CREDENTIALS_ALERT, timeout)

    def dismiss_alert(self) -> None:
        self.click(_ALERT_CONFIRM_BUTTON)
