from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver

from config.app_config import AppConfig
from pages.base_page import BasePage

# 홈 앱바 우측 상단 장바구니 아이콘 - Compose UI라 resource-id/content-desc가 없어서
# 앱바 내 클릭 가능한 두 아이콘(알림센터, 장바구니) 중 순서로 특정한다(접근성 라벨 부재는
# 실제 앱의 접근성 미비 지점 - 상품 상세 화면의 동일 기능 아이콘은 content-desc="cart"가 있음).
_CART_ICON = (
    AppiumBy.XPATH,
    '(//*[@resource-id="com.dbs.kurly.m2:id/appbar"]//android.widget.FrameLayout[@clickable="true"])[2]',
)
_CART_TITLE = (
    AppiumBy.XPATH,
    "//*[@resource-id='topBar']//android.widget.TextView[@text='장바구니']",
)
_CLOSE_BUTTON = (AppiumBy.XPATH, "//*[@resource-id='closeButton']")
_EMPTY_CART_MSG = (AppiumBy.XPATH, "//*[@text='담은 상품이 없어요']")


class CartPage(BasePage):
    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

    def open_from_home(self) -> None:
        self.click(_CART_ICON)

    def is_loaded(self, timeout: int = AppConfig.DEFAULT_TIMEOUT) -> bool:
        return self.is_visible(_CART_TITLE, timeout)

    def is_empty(self, timeout: int = AppConfig.SHORT_TIMEOUT) -> bool:
        return self.is_visible(_EMPTY_CART_MSG, timeout)

    def close(self) -> None:
        self.click(_CLOSE_BUTTON)
