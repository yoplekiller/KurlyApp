import time
from datetime import datetime
from pathlib import Path
from typing import Any
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.app_config import AppConfig
from utils.context_manager import switch_to_native, switch_to_webview
from utils.logger import get_logger

Locator = tuple[str, str]
logger = get_logger(__name__)


#   BasePage는 모든 페이지 객체의 공통 기능을 제공하는 클래스입니다.
class BasePage:
    # 페이지 객체는 Appium WebDriver 인스턴스를 받아 초기화됩니다.  
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, AppConfig.DEFAULT_TIMEOUT)

    #   find_element, find_elements, click, input_text, get_text 등은 페이지 객체에서 자주 사용되는 기본적인 요소 상호작용 메서드입니다.
    def find_element(self, locator: Locator, timeout: int | None = None) -> WebElement:
        return WebDriverWait(driver=self.driver, timeout=timeout or AppConfig.DEFAULT_TIMEOUT).until(
            EC.presence_of_element_located(locator)
        )

    def find_elements(self, locator: Locator, timeout: int | None = None) -> list[WebElement]:
        return WebDriverWait(driver=self.driver, timeout=timeout or AppConfig.DEFAULT_TIMEOUT).until(
            EC.presence_of_all_elements_located(locator)
        )

    def click(self, locator: Locator, timeout: int | None = None) -> WebElement:
        element = WebDriverWait(driver=self.driver, timeout=timeout or AppConfig.DEFAULT_TIMEOUT).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()
        logger.info("Clicked: %s", locator)
        return element

    def input_text(self, locator: Locator, text: str, timeout: int | None = None) -> WebElement:
        element = self.find_element(locator, timeout)
        element.clear()
        element.send_keys(text)
        logger.info("Input text into: %s", locator)
        return element

    def get_text(self, locator: Locator, timeout: int | None = None) -> str:
        return self.find_element(locator, timeout).text

    def is_visible(self, locator: Locator, timeout: int = AppConfig.SHORT_TIMEOUT) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def safe_click(self, locator: Locator, timeout: int = AppConfig.SHORT_TIMEOUT) -> bool:
        try:
            self.click(locator, timeout)
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def find_by_text(self, text: str, timeout: int | None = None) -> WebElement:
        selector = f'new UiSelector().text("{text}")'
        return self.find_element((AppiumBy.ANDROID_UIAUTOMATOR, selector), timeout)

    def click_by_text(self, text: str, timeout: int | None = None) -> WebElement:
        selector = f'new UiSelector().text("{text}")'
        return self.click((AppiumBy.ANDROID_UIAUTOMATOR, selector), timeout)

    def swipe_up(self, duration: int = 500) -> None:
        size = self.driver.get_window_size()
        x = size["width"] // 2
        start_y = int(size["height"] * 0.78)
        end_y = int(size["height"] * 0.25)
        self.driver.swipe(x, start_y, x, end_y, duration)
        time.sleep(0.5)

    def swipe_down(self, duration: int = 500) -> None:
        size = self.driver.get_window_size()
        x = size["width"] // 2
        start_y = int(size["height"] * 0.25)
        end_y = int(size["height"] * 0.78)
        self.driver.swipe(x, start_y, x, end_y, duration)
        time.sleep(0.5)

    def take_screenshot(self, name: str) -> str:
        AppConfig.ensure_directories()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = Path(AppConfig.SCREENSHOT_DIR) / f"{name}_{timestamp}.png"
        self.driver.get_screenshot_as_file(str(path))
        return str(path)

    def switch_to_webview(self, timeout: int = 15) -> bool:
        return switch_to_webview(self.driver, timeout)

    def switch_to_native(self) -> None:
        switch_to_native(self.driver)

    def find_element_by_css(self, css: str, timeout: int | None = None) -> WebElement:
        return WebDriverWait(self.driver, timeout or AppConfig.DEFAULT_TIMEOUT).until(
            EC.presence_of_element_located(("css selector", css))
        )

    def is_visible_by_css(self, css: str, timeout: int = AppConfig.SHORT_TIMEOUT) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(("css selector", css))
            )
            return True
        except TimeoutException:
            return False

    def find_broken_images(self, wait_for_load: bool = True) -> list[dict[str, Any]]:
        if wait_for_load:
            time.sleep(3)

        broken_images: list[dict[str, Any]] = []
        images = self.driver.find_elements(AppiumBy.XPATH, "//android.widget.ImageView")

        for index, image in enumerate(images):
            size = image.size
            if size["width"] <= 1 or size["height"] <= 1:
                broken_images.append(
                    {
                        "index": index,
                        "resource_id": image.get_attribute("resource-id"),
                        "content_desc": image.get_attribute("content-desc"),
                        "bounds": image.get_attribute("bounds"),
                        "size": size,
                        "reason": "Invalid image size",
                    }
                )

        return broken_images
