from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver

from config.app_config import AppConfig
from pages.base_page import BasePage

_SEARCH_TAB = (AppiumBy.ID, "com.dbs.kurly.m2:id/search")
_SEARCH_INPUT = (AppiumBy.XPATH, "//android.widget.EditText")
_RECOMMENDED_KEYWORDS = (AppiumBy.XPATH, "//*[@text='추천 검색어']")
# 완전 일치하는 상품이 없는 검색어를 넣어도 빈 화면이 아니라 이 문구와 함께 "관련 상품"을
# 대신 보여준다(실기기 조사로 확인 - "zzxxqqweuchsjahdsf12345" 같은 무의미한 키워드로도
# 총 80개의 관련 상품이 노출됨). 이 앱엔 완전한 "검색 결과 없음" 빈 상태 자체가 없음.
_NO_EXACT_MATCH_MSG = (
    AppiumBy.XPATH,
    "//*[contains(@text, '관련 있는 상품을 함께 보여드려요')]",
)
# 검색어를 입력하지 않고(포커스만 준 뒤) 검색을 제출하면, 검색 화면에 머물거나 안내 팝업이
# 뜨는 대신 곧바로 앱바 상단 탭 메뉴의 "이벤트"(프로모션) 웹뷰 화면으로 이동해버린다(실기기로
# 2회 재현 확인 - 웹 버전의 "검색어를 입력해주세요" 안내와 다른 동작). 이 화면은 WebView라
# 내부 콘텐츠는 Appium으로 못 보지만, 네이티브 topBar의 "이벤트" 타이틀 텍스트로 진입 여부를
# 확인할 수 있다.
_EVENT_PAGE_TITLE = (AppiumBy.XPATH, "//android.widget.TextView[@text='이벤트']")


class SearchPage(BasePage):
    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

    def navigate(self) -> None:
        if not self.is_present(_SEARCH_INPUT, timeout=2):
            self.click(_SEARCH_TAB)

    def is_loaded(self, timeout: int = AppConfig.DEFAULT_TIMEOUT) -> bool:
        return self.is_present(_SEARCH_INPUT, timeout)

    def input_text_to_search(self, keyword: str) -> None:
        self.input_text(_SEARCH_INPUT, keyword)

    def submit_search(self) -> None:
        self.driver.press_keycode(66)  # Enter

    def submit_blank_search(self) -> None:
        """검색어를 입력하지 않고 검색창에 포커스만 준 뒤 제출한다(빈 검색어 시나리오 재현용).

        포커스 없이 바로 keycode(Enter)만 누르면 검색창이 아닌 엉뚱한 요소가 눌릴 수 있어
        (실기기 조사로 확인) 반드시 입력창을 먼저 탭해서 포커스를 준 뒤 제출해야 한다.
        """
        self.click(_SEARCH_INPUT)
        self.submit_search()

    def has_results(self, keyword: str, timeout: int = AppConfig.DEFAULT_TIMEOUT) -> bool:
        locator = (AppiumBy.XPATH, f"//*[contains(@text, '{keyword}')]")
        return self.is_visible(locator, timeout)

    def has_recommended_keywords(self, timeout: int = AppConfig.DEFAULT_TIMEOUT) -> bool:
        return self.is_visible(_RECOMMENDED_KEYWORDS, timeout)

    def has_no_exact_match_message(self, timeout: int = AppConfig.DEFAULT_TIMEOUT) -> bool:
        return self.is_visible(_NO_EXACT_MATCH_MSG, timeout)

    def is_on_event_page(self, timeout: int = AppConfig.DEFAULT_TIMEOUT) -> bool:
        return self.is_visible(_EVENT_PAGE_TITLE, timeout)
