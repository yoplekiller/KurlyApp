import json
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

load_dotenv()

_DEVICE_PROFILES_PATH = Path(__file__).parent / "device_profiles.json"

# Appium 세션에 항상 붙는 공통 옵션 (기기 프로필과 무관)
_COMMON_CAPABILITIES: dict[str, Any] = {
    "noReset": True,        # 앱 데이터 유지 (재로그인 방지)
    "forceAppLaunch": True, # 앱이 닫혀 있어도 강제 실행
    "chromedriverAutodownload": True,
    "newCommandTimeout": 300,
    "keepScreenOn": True,   # 테스트 중 화면 꺼짐 방지
}


class AppConfig:
    # Groq AI
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    HEALING_ENABLED = os.getenv("HEALING_ENABLED", "true").lower() == "true"

    # Slack
    SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "")
    SLACK_NOTIFY_ENABLED = os.getenv("SLACK_NOTIFY_ENABLED", "true").lower() == "true"

    # Appium 서버 및 타임아웃 설정
    APPIUM_SERVER_URL = os.getenv("APPIUM_SERVER_URL", "http://127.0.0.1:4723")
    DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "10"))
    SHORT_TIMEOUT = int(os.getenv("SHORT_TIMEOUT", "5"))
    LONG_TIMEOUT = int(os.getenv("LONG_TIMEOUT", "30"))
    POPUP_WAIT = float(os.getenv("POPUP_WAIT", "8"))

    # 실행할 기기 프로필 (device_profiles.json의 키) — --device-profile CLI 옵션으로 재정의 가능
    DEVICE_PROFILE = os.getenv("DEVICE_PROFILE", "galaxy_a23")

    # 아티팩트 저장 경로
    SCREENSHOT_DIR = "screenshots"
    PAGE_SOURCE_DIR = "page_sources"
    LOG_DIR = "logs"

    @staticmethod
    def load_device_profiles() -> dict[str, dict[str, Any]]:
        with open(_DEVICE_PROFILES_PATH, encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def get_capabilities(profile_name: str | None = None) -> dict[str, Any]:
        """Appium 세션 생성에 필요한 capabilities를 반환한다.

        profile_name을 생략하면 AppConfig.DEVICE_PROFILE(기본값 또는 --device-profile로
        정해진 값)을 사용한다. device_profiles.json에 프로필을 추가하면 여러 기기를
        번갈아/병렬로 테스트할 수 있다.
        """
        profiles = AppConfig.load_device_profiles()
        name = profile_name or AppConfig.DEVICE_PROFILE
        profile = profiles.get(name)
        if profile is None:
            raise RuntimeError(
                f"알 수 없는 기기 프로필: {name!r} "
                f"(device_profiles.json에 등록된 프로필: {list(profiles)})"
            )

        # appActivity처럼 의도적으로 비워둔 값("")은 Appium 기본 launcher activity 사용을 위해 제외
        capabilities: dict[str, Any] = {k: v for k, v in profile.items() if v}
        capabilities.update(_COMMON_CAPABILITIES)
        return capabilities

    @staticmethod
    def ensure_directories() -> None:
        """스크린샷, 페이지소스, 로그 저장 디렉터리를 생성한다."""
        for path in (AppConfig.SCREENSHOT_DIR, AppConfig.PAGE_SOURCE_DIR, AppConfig.LOG_DIR):
            os.makedirs(path, exist_ok=True)
