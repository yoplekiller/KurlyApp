import time
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.logger import get_logger

logger = get_logger(__name__)

_HOME_LOCATOR = (AppiumBy.ID, "com.dbs.kurly.m2:id/bottom_navigation")


def _is_home(driver: WebDriver, timeout: float = 2) -> bool:
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located(_HOME_LOCATOR))
        return True
    except (TimeoutException, WebDriverException):
        return False


def handle_kurly_popups(driver: WebDriver, wait_time: float = 8) -> None:
    if _is_home(driver, wait_time):
        return

    for _ in range(5):
        try:
            closed = _close_permission_popup(driver) or _close_kurly_popup(driver)
        except WebDriverException as e:
            logger.warning("Popup handler error: %s", e)
            break
        if not closed:
            break
        time.sleep(1.0)
        if _is_home(driver, 3):
            return

    # 마지막 수단: 뒤로가기 한 번
    try:
        driver.press_keycode(4)
        time.sleep(1.0)
        if _is_home(driver, 5):
            return
    except WebDriverException:
        pass

    # 앱이 종료됐으면 재활성화
    try:
        driver.activate_app("com.dbs.kurly.m2")
        _is_home(driver, 8)
    except WebDriverException:
        pass


def _close_permission_popup(driver: WebDriver, timeout: float = 0.5) -> bool:
    locators = [
        (AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_button"),
        (AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_foreground_only_button"),
    ]
    for locator in locators:
        try:
            WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator)).click()
            logger.info("Permission accepted: %s", locator)
            return True
        except (TimeoutException, NoSuchElementException, WebDriverException):
            continue
    return False


def _close_kurly_popup(driver: WebDriver, timeout: float = 0.5) -> bool:
    locators = [
        (AppiumBy.ID, "com.dbs.kurly.m2:id/denyButton"),
        (AppiumBy.ID, "com.dbs.kurly.m2:id/negativeButton"),
        (AppiumBy.ID, "com.dbs.kurly.m2:id/btnNegative"),  # 로그인 유도 팝업 거부
        (AppiumBy.ID, "com.dbs.kurly.m2:id/closeButton"),  # 라이브 커머스 닫기
        (AppiumBy.XPATH, "//*[contains(@text, '보지 않기')]"),
        # 신규 회원가입 유도 쿠폰 팝업 - WebView를 감싼 OS 기본 AlertDialog라 앱 id가 아닌
        # android:id/button1을 씀. resource-id만으로는 다른 다이얼로그의 확인 버튼과 겹칠 수
        # 있어 text="닫기"까지 같이 확인(무조건 button1을 누르지 않도록 안전장치).
        (AppiumBy.XPATH, "//*[@resource-id='android:id/button1' and @text='닫기']"),
    ]
    for locator in locators:
        try:
            WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator)).click()
            logger.info("Popup closed: %s", locator)
            return True
        except (TimeoutException, NoSuchElementException, WebDriverException):
            continue
    return False
