from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage, Locator


class KurlyAppHomePage(BasePage):
    # native 탭바 (하단 네비게이션)
    SEARCH_TAB: Locator = (AppiumBy.ID, "com.dbs.kurly.m2:id/search")
    CATEGORY_TAB: Locator = (AppiumBy.ID, "com.dbs.kurly.m2:id/category")
    MY_KURLY_TAB: Locator = (AppiumBy.ID, "com.dbs.kurly.m2:id/mykurly")
    CART_BUTTON: Locator = (AppiumBy.XPATH, "//*[@resource-id='cartButton']")

    # WebView 내부 콘텐츠 (CSS selector)
    _WV_PRODUCT_CARD = "a[href*='/goods/']"

    def is_loaded(self) -> bool:
        """native 탭바 또는 WebView 상품 카드 노출 여부로 로딩 확인"""
        if self.is_visible(self.SEARCH_TAB) or self.is_visible(self.CATEGORY_TAB):
            return True
        if self.switch_to_webview(timeout=10):
            result = self.is_visible_by_css(self._WV_PRODUCT_CARD)
            self.switch_to_native()
            return result
        return False

    def has_products(self) -> bool:
        """홈 화면에 상품 카드가 1개 이상 노출되는지 확인"""
        if not self.switch_to_webview():
            return False
        result = self.is_visible_by_css(self._WV_PRODUCT_CARD)
        self.switch_to_native()
        return result

    def go_to_search(self) -> None:
        self.switch_to_native()
        self.click(self.SEARCH_TAB)

    def go_to_category(self) -> None:
        self.switch_to_native()
        self.click(self.CATEGORY_TAB)

    def go_to_my_kurly(self) -> None:
        self.switch_to_native()
        self.click(self.MY_KURLY_TAB)

    def open_cart(self) -> None:
        self.switch_to_native()
        self.click(self.CART_BUTTON)
