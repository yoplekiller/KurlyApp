from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage, Locator


class KurlyAppCartPage(BasePage):
    CART_TITLE: Locator = (
        AppiumBy.XPATH,
        "//*[contains(@text, '장바구니') or contains(@content-desc, '장바구니')]",
    )

    def is_loaded(self) -> bool:
        return self.is_visible(self.CART_TITLE)
