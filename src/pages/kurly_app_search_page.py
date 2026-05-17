from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from pages.base_page import BasePage, Locator


class KurlyAppSearchPage(BasePage):
    # native 검색 입력창 (검색 탭 진입 후 활성화되는 native input)
    SEARCH_INPUT: Locator = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'search') or contains(@text, '검색어를 입력') or contains(@hint, '검색')]",
    )

    # WebView 내부 결과
    _WV_PRODUCT_LINK = "a[href*='/goods/']"
    _WV_RESULT_COUNT = "[class*='count'], [class*='Count'], [class*='result']"
    _WV_NO_RESULT = "[class*='empty'], [class*='Empty'], [class*='noResult']"

    def search(self, keyword: str) -> None:
        self.switch_to_native()
        try:
            self.click(self.SEARCH_INPUT)
        except (TimeoutException, NoSuchElementException):
            pass
        active = self.driver.switch_to.active_element
        active.send_keys(keyword)
        self.driver.press_keycode(66)  # Enter

    def has_results(self) -> bool:
        """검색 결과 상품이 1개 이상 노출되는지 확인 (WebView)"""
        if not self.switch_to_webview():
            return False
        result = self.is_visible_by_css(self._WV_PRODUCT_LINK)
        self.switch_to_native()
        return result

    def is_no_result(self) -> bool:
        """검색 결과 없음 상태 확인 (WebView)"""
        if not self.switch_to_webview():
            return False
        result = self.is_visible_by_css(self._WV_NO_RESULT)
        self.switch_to_native()
        return result
