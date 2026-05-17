from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage, Locator


class KurlyAppCartPage(BasePage):
    # native topBar 제목
    CART_TITLE: Locator = (
        AppiumBy.XPATH,
        "//*[@resource-id='topBar']//android.widget.TextView[@text='장바구니']",
    )
    CLOSE_BUTTON: Locator = (
        AppiumBy.XPATH,
        "//*[@resource-id='closeButton']",
    )
    # WebView 내 요소 (Android 접근성 트리로 노출)
    EMPTY_CART_MSG: Locator = (
        AppiumBy.XPATH,
        "//*[@text='담은 상품이 없어요']",
    )

    def is_loaded(self) -> bool:
        return self.is_visible(self.CART_TITLE)

    def is_empty(self) -> bool:
        return self.is_visible(self.EMPTY_CART_MSG)

    def close(self) -> None:
        self.switch_to_native()
        self.click(self.CLOSE_BUTTON)
