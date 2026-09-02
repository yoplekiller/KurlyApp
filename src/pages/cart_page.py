from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver

from config.app_config import AppConfig
from pages.base_page import BasePage

# 홈 앱바 우측 상단 장바구니 아이콘 - Compose UI라 resource-id/content-desc가 없어서
# 앱바 내 클릭 가능한 두 아이콘(알림센터, 장바구니) 중 순서로 특정한다(접근성 라벨 부재는
# 실제 앱의 접근성 미비 지점 - 상품 상세 화면의 동일 기능 아이콘은 content-desc="cart"가 있음).
# (2026-09-02 갱신) 앱바가 Jetpack Compose로 마이그레이션되며 위젯 클래스가
# android.widget.FrameLayout -> android.view.View로 바뀌어 기존 로케이터가 깨짐. 주의: appbar
# 하위엔 clickable View가 10개 있음(상단 아이콘 5개 + 그 아래 카테고리 탭 5개, 실기기 조사로 확인) -
# last()를 쓰면 카테고리 탭을 잘못 클릭하게 됨. 상단 5개[토글,마켓컬리,뷰티컬리,알림벨,장바구니] 중
# 5번째(장바구니, 화면 최우측, bounds x:933~1080)를 position()으로 명시 지정.
_CART_ICON = (
    AppiumBy.XPATH,
    '(//*[@resource-id="com.dbs.kurly.m2:id/appbar"]//android.view.View[@clickable="true"])[5]',
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
