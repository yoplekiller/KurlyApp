from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage, Locator


class KurlyAppMyTabPage(BasePage):
    MY_TAB_SELECTED: Locator = (
        AppiumBy.XPATH,
        "//android.widget.FrameLayout[@resource-id='com.dbs.kurly.m2:id/mykurly' and @selected='true']",
    )
    LOGIN_ENTRY: Locator = (
        AppiumBy.XPATH,
        "//*[contains(@text, '로그인') or contains(@content-desc, '로그인')]",
    )
    ORDER_HISTORY: Locator = (AppiumBy.XPATH, "//*[@content-desc='주문 내역']")

    def is_loaded(self) -> bool:
        return self.is_visible(self.MY_TAB_SELECTED)

    def go_to_login(self) -> None:
        self.click(self.LOGIN_ENTRY)

    def requires_login(self) -> bool:
        return self.is_visible(self.LOGIN_ENTRY)

    def is_logged_in(self) -> bool:
        return self.is_visible(self.ORDER_HISTORY)
