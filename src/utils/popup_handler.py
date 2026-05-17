import time

from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.context_manager import NATIVE, switch_to_native
from utils.logger import get_logger

logger = get_logger(__name__)


def handle_kurly_popups(driver: WebDriver, wait_time: float = 2) -> None:
    switch_to_native(driver)
    try:
        WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((AppiumBy.ID, "com.dbs.kurly.m2:id/bottom_navigation"))
        )
    except TimeoutException:
        pass
    _allow_android_permissions(driver)
    _close_common_popups(driver)


def _allow_android_permissions(driver: WebDriver, timeout: int = 3) -> None:
    permission_buttons = [
        (AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_button"),
        (AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_foreground_only_button"),
        (AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_all_button"),
        (AppiumBy.ID, "com.android.packageinstaller:id/permission_allow_button"),
    ]

    for locator in permission_buttons:
        try:
            WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable(locator)
            ).click()
            logger.info("Android permission popup accepted: %s", locator)
        except (TimeoutException, NoSuchElementException):
            continue


def _close_common_popups(driver: WebDriver, timeout: int = 2) -> None:
    close_locators = [
        (AppiumBy.ACCESSIBILITY_ID, "닫기"),
        (AppiumBy.ACCESSIBILITY_ID, "close"),
        (AppiumBy.XPATH, "//*[@text='닫기']"),
        (AppiumBy.XPATH, "//*[@text='오늘 하루 보지 않기']"),
        (AppiumBy.XPATH, "//*[contains(@text, '닫기')]"),
        (AppiumBy.XPATH, "//*[contains(@content-desc, '닫기')]"),
        (AppiumBy.XPATH, "//*[contains(@resource-id, 'close')]"),
    ]

    for locator in close_locators:
        try:
            WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable(locator)
            ).click()
            logger.info("Popup closed: %s", locator)
            time.sleep(0.5)
        except (TimeoutException, NoSuchElementException):
            continue
