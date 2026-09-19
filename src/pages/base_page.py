import time
from datetime import datetime
from pathlib import Path
from typing import Any
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from groq import Groq
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.app_config import AppConfig
from utils.logger import get_logger
from utils.self_healer import suggest_locator

Locator = tuple[str, str]
logger = get_logger(__name__)

_groq_client: Groq | None = Groq(api_key=AppConfig.GROQ_API_KEY) if AppConfig.GROQ_API_KEY else None


class BasePage:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, AppConfig.DEFAULT_TIMEOUT)

    def find_element(self, locator: Locator, timeout: int | None = None) -> WebElement:
        try:
            return WebDriverWait(driver=self.driver, timeout=timeout or AppConfig.DEFAULT_TIMEOUT).until(
                EC.presence_of_element_located(locator)
            )
        except (TimeoutException, NoSuchElementException):
            healed = self._try_heal(locator) if AppConfig.HEALING_ENABLED else None
            if healed is not None:
                return healed
            raise

    def _try_heal(self, original_locator: Locator) -> WebElement | None:
        if _groq_client is None:
            logger.warning("Self-healing skipped: GROQ_API_KEY not set")
            return None
        try:
            logger.warning("Self-healing triggered for locator: %s", original_locator)
            page_source = self.driver.page_source
            new_locator = suggest_locator(original_locator, page_source, _groq_client)
            if new_locator is None:
                return None
            element = WebDriverWait(self.driver, AppConfig.SHORT_TIMEOUT).until(
                EC.presence_of_element_located(new_locator)
            )
            logger.info("Self-healed: %s → %s", original_locator, new_locator)
            return element
        except Exception as e:
            logger.warning("Self-healing failed: %s", e)
            return None

    def find_elements(self, locator: Locator, timeout: int | None = None) -> list[WebElement]:
        return WebDriverWait(driver=self.driver, timeout=timeout or AppConfig.DEFAULT_TIMEOUT).until(
            EC.presence_of_all_elements_located(locator)
        )

    def click(self, locator: Locator, timeout: int | None = None) -> WebElement:
        try:
            element = WebDriverWait(driver=self.driver, timeout=timeout or AppConfig.DEFAULT_TIMEOUT).until(
                EC.element_to_be_clickable(locator)
            )
        except (TimeoutException, NoSuchElementException):
            healed = self._try_heal(locator) if AppConfig.HEALING_ENABLED else None
            if healed is None:
                raise
            element = healed
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

    def is_present(self, locator: Locator, timeout: int = AppConfig.SHORT_TIMEOUT) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
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
        self._w3c_swipe(
            start_x=x,
            start_y=int(size["height"] * 0.78),
            end_x=x,
            end_y=int(size["height"] * 0.25),
            duration=duration,
        )

    def swipe_down(self, duration: int = 500) -> None:
        size = self.driver.get_window_size()
        x = size["width"] // 2
        self._w3c_swipe(
            start_x=x,
            start_y=int(size["height"] * 0.25),
            end_x=x,
            end_y=int(size["height"] * 0.78),
            duration=duration,
        )

    def _w3c_swipe(
        self,
        start_x: int,
        start_y: int,
        end_x: int,
        end_y: int,
        duration: int = 500,
    ) -> None:
        finger = PointerInput(interaction.POINTER_TOUCH, "finger")
        actions = ActionBuilder(self.driver, mouse=finger)
        actions.pointer_action.move_to_location(start_x, start_y)
        actions.pointer_action.pointer_down()
        actions.pointer_action.pause(duration / 1000)
        actions.pointer_action.move_to_location(end_x, end_y)
        actions.pointer_action.release()
        actions.perform()

    def take_screenshot(self, name: str) -> str:
        AppConfig.ensure_directories()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = Path(AppConfig.SCREENSHOT_DIR) / f"{name}_{timestamp}.png"
        self.driver.get_screenshot_as_file(str(path))
        return str(path)

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
            try:
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
            except StaleElementReferenceException:
                # 홈 배너(ViewPager)가 자동 회전하며 순회 중인 ImageView를 교체하는 경우 발생.
                # 요소가 사라진 것뿐이라 "깨진 이미지"가 아니므로 건너뛴다.
                continue

        return broken_images
