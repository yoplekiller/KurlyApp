from datetime import datetime
from pathlib import Path

from appium.webdriver.webdriver import WebDriver

from config.app_config import AppConfig


def save_page_source(driver: WebDriver, prefix: str = "page_source") -> str:
    AppConfig.ensure_directories()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = Path(AppConfig.PAGE_SOURCE_DIR) / f"{prefix}_{timestamp}.xml"
    path.write_text(driver.page_source, encoding="utf-8")
    return str(path)
