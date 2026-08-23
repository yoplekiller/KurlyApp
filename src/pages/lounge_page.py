from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver

from config.app_config import AppConfig
from pages.base_page import BasePage

_LOUNGE_TAB = (AppiumBy.ID, "com.dbs.kurly.m2:id/lounge")
_LOUNGE_TITLE = (AppiumBy.XPATH, "//*[@text='라운지']")
_ALL_CONTENT_TAB = (AppiumBy.XPATH, "//*[@text='전체 콘텐츠']")


class LoungePage(BasePage):
    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

    def navigate(self) -> None:
        self.click(_LOUNGE_TAB)

    def is_loaded(self, timeout: int = AppConfig.LONG_TIMEOUT) -> bool:
        # 웹뷰 기반 화면이라 로딩에 시간이 좀 더 걸린다.
        return self.is_visible(_LOUNGE_TITLE, timeout)

    def has_content_tabs(self, timeout: int = AppConfig.DEFAULT_TIMEOUT) -> bool:
        return self.is_visible(_ALL_CONTENT_TAB, timeout)
