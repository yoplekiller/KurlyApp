from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver

from config.app_config import AppConfig
from pages.base_page import BasePage

_CATEGORY_TAB = (AppiumBy.ID, "com.dbs.kurly.m2:id/category")
_MARKET_KURLY_TAB = (AppiumBy.XPATH, "//*[@text='마켓컬리']")
_BEAUTY_KURLY_TAB = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("뷰티컬리").instance(0)')
_CATEGORY_ITEM = (AppiumBy.XPATH, "//*[@clickable='true' and @focusable='true']/android.widget.TextView[@text='채소']")


class CategoryPage(BasePage):
    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

    def navigate(self) -> None:
        for _ in range(3):
            if self.is_present(_CATEGORY_TAB, timeout=2):
                break
            self.driver.press_keycode(4)  # Back key to dismiss fullscreen overlay (e.g. search screen)
        self.click(_CATEGORY_TAB)
        # noReset=True로 인해 이전 세션에서 뷰티컬리 서브탭을 선택한 상태가 남아있을 수 있어
        # 항상 마켓컬리 서브탭으로 명시적으로 맞춰준다.
        self.click(_MARKET_KURLY_TAB)

    def is_loaded(self, timeout: int = AppConfig.DEFAULT_TIMEOUT) -> bool:
        return self.is_visible(_MARKET_KURLY_TAB, timeout)

    def has_category_list(self, timeout: int = AppConfig.DEFAULT_TIMEOUT) -> bool:
        return self.is_visible(_CATEGORY_ITEM, timeout)

    def has_beauty_tab(self, timeout: int = AppConfig.DEFAULT_TIMEOUT) -> bool:
        return self.is_visible(_BEAUTY_KURLY_TAB, timeout)

    def switch_to_beauty(self) -> None:
        self.click(_BEAUTY_KURLY_TAB)
