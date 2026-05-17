import os
from datetime import datetime
from typing import Generator

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.webdriver import WebDriver

from config.app_config import AppConfig
from pages.kurly_app_cart_page import KurlyAppCartPage
from pages.kurly_app_category_page import KurlyAppCategoryPage
from pages.kurly_app_home_page import KurlyAppHomePage
from pages.kurly_app_login_page import KurlyAppLoginPage
from pages.kurly_app_my_tab_page import KurlyAppMyTabPage
from pages.kurly_app_search_page import KurlyAppSearchPage
from utils.logger import get_logger
from utils.popup_handler import handle_kurly_popups

logger = get_logger(__name__)


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment() -> Generator[None, None, None]:
    AppConfig.ensure_directories()
    logger.info("Kurly test environment is ready")
    yield


@pytest.fixture(scope="function")
def driver() -> Generator[WebDriver, None, None]:
    options = UiAutomator2Options().load_capabilities(AppConfig.get_capabilities())
    appium_driver = webdriver.Remote(AppConfig.APPIUM_SERVER_URL, options=options)
    handle_kurly_popups(appium_driver, wait_time=AppConfig.POPUP_WAIT)

    yield appium_driver

    appium_driver.quit()


@pytest.fixture(scope="function")
def home_page(driver: WebDriver) -> KurlyAppHomePage:
    return KurlyAppHomePage(driver)


@pytest.fixture(scope="function")
def search_page(driver: WebDriver) -> KurlyAppSearchPage:
    return KurlyAppSearchPage(driver)


@pytest.fixture(scope="function")
def category_page(driver: WebDriver) -> KurlyAppCategoryPage:
    return KurlyAppCategoryPage(driver)


@pytest.fixture(scope="function")
def my_tab_page(driver: WebDriver) -> KurlyAppMyTabPage:
    return KurlyAppMyTabPage(driver)


@pytest.fixture(scope="function")
def login_page(driver: WebDriver) -> KurlyAppLoginPage:
    return KurlyAppLoginPage(driver)


@pytest.fixture(scope="function")
def cart_page(driver: WebDriver) -> KurlyAppCartPage:
    return KurlyAppCartPage(driver)


@pytest.fixture(scope="function")
def test_user_credentials() -> dict[str, str | None]:
    return {
        "user_id": os.getenv("TEST_USER_ID"),
        "password": os.getenv("TEST_USER_PASSWORD"),
    }


@pytest.fixture(scope="function")
def wrong_user_credentials() -> dict[str, str | None]:
    return {
        "user_id": os.getenv("WRONG_TEST_USER_ID"),
        "password": os.getenv("WRONG_TEST_USER_PASSWORD"),
    }


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or not report.failed or "driver" not in item.funcargs:
        return

    appium_driver = item.funcargs["driver"]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    test_name = item.nodeid.replace("::", "_").replace("/", "_").replace("\\", "_")

    screenshot_path = os.path.join(AppConfig.SCREENSHOT_DIR, f"FAILED_{test_name}_{timestamp}.png")
    source_path = os.path.join(AppConfig.PAGE_SOURCE_DIR, f"FAILED_{test_name}_{timestamp}.xml")

    appium_driver.get_screenshot_as_file(screenshot_path)
    with open(source_path, "w", encoding="utf-8") as file:
        file.write(appium_driver.page_source)

    logger.error("Failure artifacts saved: %s, %s", screenshot_path, source_path)
