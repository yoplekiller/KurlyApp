from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from config.app_config import AppConfig
from pages.base_page import BasePage

_BOTTOM_NAV = (AppiumBy.ID, "com.dbs.kurly.m2:id/bottom_navigation")
_HOME_TAB = (AppiumBy.ID, "com.dbs.kurly.m2:id/home")
_PRODUCT_ITEM = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("베스트")')
_BANNER = (AppiumBy.XPATH, "//androidx.viewpager2.widget.ViewPager2 | //androidx.viewpager.widget.ViewPager")


class HomePage(BasePage):
    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

    def navigate(self) -> None:
        if not self.is_present(_HOME_TAB, timeout=2):
            self.driver.press_keycode(4)  # Back key to dismiss fullscreen overlay (e.g. search screen)
        self.click(_HOME_TAB)

    def is_loaded(self, timeout: int = AppConfig.DEFAULT_TIMEOUT) -> bool:
        return self.is_visible(_BOTTOM_NAV, timeout)

    def has_products(self, timeout: int = AppConfig.DEFAULT_TIMEOUT) -> bool:
        return self.is_visible(_PRODUCT_ITEM, timeout)

    def open_best_products(self) -> None:
        self.click(_PRODUCT_ITEM)

    def open_product(self, keyword: str) -> None:
        locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().textContains("{keyword}")')
        self.click(locator)

    def has_banner(self, timeout: int = AppConfig.SHORT_TIMEOUT) -> bool:
        return self.is_visible(_BANNER, timeout)

    def scroll_down(self) -> None:
        self.swipe_up()

    def scroll_up(self) -> None:
        self.swipe_down()
