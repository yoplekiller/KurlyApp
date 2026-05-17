import time

from appium.webdriver.webdriver import WebDriver

from utils.logger import get_logger

logger = get_logger(__name__)

NATIVE = "NATIVE_APP"

#  context_manager.py는 Appium 테스트에서 네이티브 앱과 웹뷰 간의 컨텍스트 전환을 관리하는 유틸리티 함수들을 제공합니다.
def get_webview_context(driver: WebDriver, timeout: int = 15) -> str | None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        for ctx in driver.contexts:
            if ctx.startswith("WEBVIEW_"):
                return ctx
        time.sleep(1)
    logger.warning("No WebView context found within %ds", timeout)
    return None


def switch_to_webview(driver: WebDriver, timeout: int = 15) -> bool:
    ctx = get_webview_context(driver, timeout)
    if ctx:
        driver.switch_to.context(ctx)
        logger.info("Switched to context: %s", ctx)
        return True
    return False


def switch_to_native(driver: WebDriver) -> None:
    driver.switch_to.context(NATIVE)
    logger.info("Switched to NATIVE_APP context")
