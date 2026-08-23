from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver

from config.app_config import AppConfig
from pages.base_page import BasePage

_PICK_BUTTON = (AppiumBy.ID, "com.dbs.kurly.m2:id/pick_button_container")
_LOGIN_PROMPT_MESSAGE = (
    AppiumBy.ANDROID_UIAUTOMATOR,
    'new UiSelector().textContains("로그인 후 찜할 수 있어요")',
)
_LOGIN_PROMPT_CANCEL = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("취소")')


class ProductDetailPage(BasePage):
    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

    def tap_pick_button(self) -> None:
        self.click(_PICK_BUTTON)

    def has_login_prompt(self, timeout: int = AppConfig.DEFAULT_TIMEOUT) -> bool:
        return self.is_visible(_LOGIN_PROMPT_MESSAGE, timeout)

    def cancel_login_prompt(self) -> None:
        self.click(_LOGIN_PROMPT_CANCEL)
