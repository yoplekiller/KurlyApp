import time

from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from selenium.common.exceptions import StaleElementReferenceException

from config.app_config import AppConfig
from pages.base_page import BasePage

_BOTTOM_NAV = (AppiumBy.ID, "com.dbs.kurly.m2:id/bottom_navigation")
_HOME_TAB = (AppiumBy.ID, "com.dbs.kurly.m2:id/home")
_PRODUCT_ITEM = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("베스트")')
_BANNER = (AppiumBy.XPATH, "//androidx.viewpager2.widget.ViewPager2 | //androidx.viewpager.widget.ViewPager")
# 목록의 첫 상품 카드 전체(제목/가격을 감싸는 클릭 가능한 View) - 가격 텍스트("~원")를 기준으로
# 가장 가까운 clickable 조상을 찾는다. 실기기 조사로 확인: 카드 내부의 "담기" 퀵버튼도 별도
# clickable View라 가격 텍스트 기준으로 잡아야 퀵버튼과 겹치지 않고 카드 전체(상세 진입용)를 집는다.
# 특정 상품명을 하드코딩하지 않기 위한 용도 - 베스트 상품 구성이 바뀌어도 깨지지 않음.
_ANY_PRODUCT_CARD = (
    AppiumBy.XPATH,
    "(//android.widget.TextView[contains(@text,'원')]/ancestor::android.view.View[@clickable='true'][1])[1]",
)
# 목록 카드 내 "담기" 퀵버튼 - 누르면 옵션/수량 선택 바텀시트가 뜬다(장바구니에 바로 담기지 않음).
_QUICK_ADD_BUTTON = (
    AppiumBy.XPATH,
    "(//android.widget.TextView[@text='담기']/ancestor::android.view.View[@clickable='true'][1])[1]",
)
# 아래 3개는 퀵 담기 바텀시트 내부 컨트롤 - 전부 실기기 조사로 확인한 고유 resource-id.
# 실기기 조사로 확인된 주의사항: 수량을 올리지 않고(0개) 바로 확정하면 "최소 구매 수량은 1개
# 입니다" 알림이 뜨며 담기가 막힌다 - 반드시 수량을 1 이상으로 올린 후 확정해야 한다.
_QTY_INCREASE_BUTTON = (AppiumBy.ID, "com.dbs.kurly.m2:id/increaseButton")
_CONFIRM_ADD_TO_CART_BUTTON = (AppiumBy.ID, "com.dbs.kurly.m2:id/btnAddToCard")
# 담기 확정 후 "함께 구매하면 좋을 상품" 크로스셀 바텀시트가 항상 뜬다. 뒤로가기(keycode 4)는
# 이 화면에서 앱을 통째로 종료시켜버리므로 사용하면 안 된다(실기기로 직접 확인한 회귀).
#
# 주의(실기기 조사로 확인, 2026-09-15): touch_outside(scrim) 뷰의 bounds가 [0,80]~[1080,2400]로
# 시트 패널(design_bottom_sheet, bounds [0,872]~[1080,2400])까지 통째로 덮고 있어서, 이 요소를
# element.click()으로 누르면 Appium이 bounds의 "중심점"을 탭하는데 그 좌표가 시트 자체(패널
# 내부)에 찍혀버려 실제로는 안 닫힘 - 이게 그동안 배지 카운트가 안 맞던 근본 원인이었음. 대신
# 시트 패널의 실제 top 좌표를 읽어서 화면 상단~시트 top 사이(진짜 빈 scrim 영역)의 중간 지점을
# 좌표로 직접 tap한다.
_CROSS_SELL_SHEET_PANEL = (AppiumBy.ID, "com.dbs.kurly.m2:id/design_bottom_sheet")
# 담기 확정 시 크로스셀 시트 안에 항상 뜨는 네이티브 확인 메시지 - 이미 장바구니에 있는 상품을
# 다시 담아도(수량만 올라가고 배지의 "고유 상품 개수"는 안 늘어남, 실기기 조사로 확인) 매번 뜨므로
# 장바구니 배지 숫자보다 "담기 자체가 성공했는지"를 훨씬 안정적으로 증명하는 신호다.
_ADD_CONFIRMATION_MSG = (AppiumBy.ID, "com.dbs.kurly.m2:id/tvCompleteAddMessage")


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
        """특정 상품명에 의존하지 않고 목록의 첫 상품 상세로 진입한다.

        베스트 상품 구성이 바뀌어도 깨지지 않아야 하는 테스트(찜하기 등)에서 사용한다.
        """
        self.click(_ANY_PRODUCT_CARD)

    def quick_add_first_product_to_cart(self) -> bool:
        """목록 첫 상품을 퀵 담기 버튼으로 장바구니에 1개 담는다(상세 진입 없이).

        담기 -> 수량 1로 증가 -> 담기 확정 -> 확정 후 뜨는 크로스셀 바텀시트 안의 담기 확인
        메시지 노출 여부 확인 -> 시트 닫기까지 한 번에 처리한다. 담기 확인 메시지가 실제로
        노출됐는지(bool)를 반환한다 - 이미 장바구니에 있는 상품이라 배지 숫자가 그대로여도
        "담기 자체는 성공했는지"를 이 반환값으로 판단할 수 있다.
        """
        self.click(_QUICK_ADD_BUTTON)
        self.click(_QTY_INCREASE_BUTTON)
        self.click(_CONFIRM_ADD_TO_CART_BUTTON)
        confirmed = self.is_visible(_ADD_CONFIRMATION_MSG, timeout=5)
        self._dismiss_cross_sell_sheet()
        return confirmed

    def _dismiss_cross_sell_sheet(self) -> None:
        # 바텀시트가 뜨는 애니메이션 도중 뷰가 재생성되면서 StaleElementReferenceException이
        # 실기기에서 간헐적으로 발생함(확인됨) - 안정될 시간을 준 뒤 1회 재시도한다.
        time.sleep(1)
        try:
            panel = self.find_element(_CROSS_SELL_SHEET_PANEL, timeout=5)
        except StaleElementReferenceException:
            panel = self.find_element(_CROSS_SELL_SHEET_PANEL, timeout=5)

        # 시트 패널의 실제 top 좌표와 화면 상단(0) 사이의 중간점을 tap한다 - 그 구간은
        # 시트가 가리지 않는 진짜 빈 scrim 영역임(실기기로 검증됨).
        sheet_top = panel.location["y"]
        screen_width = self.driver.get_window_size()["width"]
        self.driver.tap([(screen_width // 2, sheet_top // 2)])

        # 시트를 닫은 직후 appbar 배지 숫자가 갱신되기까지 약간의 지연이 있음(실기기 확인) -
        # 호출 직후 바로 배지를 읽는 코드가 과거 값을 보는 걸 방지.
        time.sleep(1.5)

    def has_banner(self, timeout: int = AppConfig.SHORT_TIMEOUT) -> bool:
        return self.is_visible(_BANNER, timeout)

    def scroll_down(self) -> None:
        self.swipe_up()

    def scroll_up(self) -> None:
        self.swipe_down()
