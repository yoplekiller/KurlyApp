from typing import Generator

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.webdriver import WebDriver
from groq import Groq

from config.app_config import AppConfig
from utils.failure_analyzer import analyze_failure
from utils.popup_handler import handle_kurly_popups
from utils.slack_notifier import send_failure_alert
from utils.logger import get_logger

logger = get_logger(__name__)

_groq_client: Groq | None = Groq(api_key=AppConfig.GROQ_API_KEY) if AppConfig.GROQ_API_KEY else None


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--device-profile",
        action="store",
        default=None,
        help="device_profiles.json에 등록된 기기 프로필 이름 (기본값: .env의 DEVICE_PROFILE)",
    )


def pytest_runtest_logreport(report: pytest.TestReport) -> None:
    if not (report.when == "call" and report.failed):
        return
    if not (AppConfig.SLACK_NOTIFY_ENABLED and _groq_client):
        return

    test_name = report.nodeid
    error_message = str(report.longrepr) if report.longrepr else "Unknown error"

    try:
        ai_analysis = analyze_failure(test_name, error_message, _groq_client)
    except Exception as e:
        logger.warning("AI 분석 실패: %s", e)
        ai_analysis = "AI 분석을 수행할 수 없습니다."

    send_failure_alert(
        test_name=test_name,
        error_summary=error_message,
        ai_analysis=ai_analysis,
    )


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment() -> Generator[None, None, None]:
    AppConfig.ensure_directories()
    logger.info("Kurly test environment is ready")
    yield


@pytest.fixture(scope="module")
def driver(request: pytest.FixtureRequest) -> Generator[WebDriver, None, None]:
    profile_name = request.config.getoption("--device-profile")
    capabilities = AppConfig.get_capabilities(profile_name)
    logger.info("Using device profile: %s", profile_name or AppConfig.DEVICE_PROFILE)

    options = UiAutomator2Options().load_capabilities(capabilities)
    appium_driver = webdriver.Remote(AppConfig.APPIUM_SERVER_URL, options=options)
    handle_kurly_popups(appium_driver, wait_time=AppConfig.POPUP_WAIT)
    yield appium_driver
    app_package = capabilities.get("appPackage", "")
    if app_package:
        appium_driver.terminate_app(app_package)
    appium_driver.quit()
