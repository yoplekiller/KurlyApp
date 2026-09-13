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

    def open_first_product(self) -> None:
        # 베스트 목록 1위 상품은 실시간 판매 데이터로 계속 바뀌므로 특정 브랜드/상품명에
        # 의존하지 않고, 모든 상품 카드에 공통으로 존재하는 가격 표시(예: "11,900원")를
        # 앵커로 삼아 첫 번째 상품을 연다. Compose 카드 자체엔 clickable 속성이 없지만
        # 가격 텍스트를 탭해도 상위 Row의 클릭이 그대로 전달되어 상세 페이지로 이동함(실기기 확인).
        locator = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textMatches(".*[0-9],[0-9]{3}원.*").instance(0)')
        self.click(locator)

    def has_banner(self, timeout: int = AppConfig.SHORT_TIMEOUT) -> bool:
        return self.is_visible(_BANNER, timeout)

    def scroll_down(self) -> None:
        self.swipe_up()

    def scroll_up(self) -> None:
        self.swipe_down()
