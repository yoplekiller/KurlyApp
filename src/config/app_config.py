import os
from typing import Any
from dotenv import load_dotenv

load_dotenv()


class AppConfig:
    APPIUM_SERVER_URL = os.getenv("APPIUM_SERVER_URL", "http://127.0.0.1:4723")

    DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "10"))
    SHORT_TIMEOUT = int(os.getenv("SHORT_TIMEOUT", "5"))
    LONG_TIMEOUT = int(os.getenv("LONG_TIMEOUT", "30"))
    POPUP_WAIT = float(os.getenv("POPUP_WAIT", "2"))

    SCREENSHOT_DIR = "screenshots"
    PAGE_SOURCE_DIR = "page_sources"
    LOG_DIR = "logs"

    @staticmethod
    def get_capabilities() -> dict[str, Any]:
        app_package = os.getenv("KURLY_APP_PACKAGE")

        if not app_package:
            raise RuntimeError("KURLY_APP_PACKAGE must be set in .env")

        capabilities: dict[str, Any] = {
            "platformName": "Android",
            "automationName": "UiAutomator2",
            "deviceName": os.getenv(
                "APPIUM_DEVICE_NAME",
                os.getenv("DEVICE_NAME", "Android"),
            ),
            "appPackage": app_package,
            "noReset": True,
            "newCommandTimeout": 300,
        }

        app_activity = os.getenv("KURLY_APP_ACTIVITY")
        if app_activity:
            capabilities["appActivity"] = app_activity

        platform_version = os.getenv(
            "APPIUM_PLATFORM_VERSION",
            os.getenv("ANDROID_PLATFORM_VERSION"),
        )
        if platform_version:
            capabilities["platformVersion"] = platform_version

        return capabilities

    @staticmethod
    def ensure_directories() -> None:
        for path in (
            AppConfig.SCREENSHOT_DIR,
            AppConfig.PAGE_SOURCE_DIR,
            AppConfig.LOG_DIR,
        ):
            os.makedirs(path, exist_ok=True)
