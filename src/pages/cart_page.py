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
# 장바구니 아이콘 우측 상단 숫자 배지. 실기기 조사로 확인: 배지 TextView는 _CART_ICON이 가리키는
# 바로 그 View의 자손이다(아이콘 컨테이너 안에 아이콘 그래픽 View 2개 + 배지를 감싸는 View 1개가
# 들어있고, 그 안에 숫자 TextView가 있음) - 그래서 _CART_ICON과 같은 position(5)을 그대로 재사용해
# 그 안의 TextView를 찾는다. (시행착오 기록: 처음엔 appbar 전체에서 "마지막 TextView"로 잡았다가
# 베스트/카테고리 등 하위 탭 화면에서는 appbar 안에 카테고리 탭 라벨(TextView)도 같이 들어있어서
# 엉뚱한 걸 집는 버그가 있었음 - 반드시 아이콘 컨테이너로 스코프를 좁혀야 함.) 담긴 상품이 없으면
# 배지 자체가 렌더링되지 않아 존재하지 않음(get_badge_count()가 0을 반환하는 이유).
#
# 주의: 장바구니 화면 내부(담긴 상품 목록/수량변경/삭제)는 WebView로 렌더링되고 원격 디버깅이
# 꺼져 있어 Appium이 그 안의 요소를 전혀 볼 수 없다(driver.contexts가 NATIVE_APP만 반환,
# 실기기 조사로 확인) - 그래서 "담기 성공 여부"를 이 배지 숫자(네이티브)로 검증한다. 수량변경/
# 삭제 자동화는 앱이 그 화면을 네이티브로 바꾸지 않는 한 Appium으로는 불가능.
_CART_BADGE_COUNT = (
    AppiumBy.XPATH,
    '((//*[@resource-id="com.dbs.kurly.m2:id/appbar"]//android.view.View[@clickable="true"])[5])'
    "//android.widget.TextView",
)


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

    def get_badge_count(self, timeout: int = AppConfig.DEFAULT_TIMEOUT) -> int:
        """appbar 장바구니 아이콘의 숫자 배지를 읽는다. 배지가 없으면(장바구니 비어있음) 0."""
        if not self.is_present(_CART_BADGE_COUNT, timeout):
            return 0
        text = self.get_text(_CART_BADGE_COUNT)
        return int(text) if text.isdigit() else 0
