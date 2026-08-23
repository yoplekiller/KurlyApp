from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver

from config.app_config import AppConfig
from pages.base_page import BasePage

_SEARCH_TAB = (AppiumBy.ID, "com.dbs.kurly.m2:id/search")
_SEARCH_INPUT = (AppiumBy.XPATH, "//android.widget.EditText")
_RECOMMENDED_KEYWORDS = (AppiumBy.XPATH, "//*[@text='추천 검색어']")


class SearchPage(BasePage):
    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

    def navigate(self) -> None:
        if not self.is_present(_SEARCH_INPUT, timeout=2):
            self.click(_SEARCH_TAB)

    def is_loaded(self, timeout: int = AppConfig.DEFAULT_TIMEOUT) -> bool:
        return self.is_present(_SEARCH_INPUT, timeout)

    def input_text_to_search(self, keyword: str) -> None:
        self.input_text(_SEARCH_INPUT, keyword)

    def submit_search(self) -> None:
        self.driver.press_keycode(66)  # Enter

    def has_results(self, keyword: str, timeout: int = AppConfig.DEFAULT_TIMEOUT) -> bool:
        locator = (AppiumBy.XPATH, f"//*[contains(@text, '{keyword}')]")
        return self.is_visible(locator, timeout)

    def has_recommended_keywords(self, timeout: int = AppConfig.DEFAULT_TIMEOUT) -> bool:
        return self.is_visible(_RECOMMENDED_KEYWORDS, timeout)
