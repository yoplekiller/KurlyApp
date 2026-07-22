"""검색 페이지 page source 덤프 - 최소한의 조작, 즉시 저장"""
import sys
sys.path.insert(0, "src")

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from utils.popup_handler import handle_kurly_popups

caps = {
    "platformName": "Android",
    "automationName": "UiAutomator2",
    "deviceName": "R59T304FH1B",
    "udid": "adb-R59T304FH1B-07Djog._adb-tls-connect._tcp",
    "appPackage": "com.dbs.kurly.m2",
    "noReset": True,
    "forceAppLaunch": True,
    "newCommandTimeout": 120,
}

options = UiAutomator2Options().load_capabilities(caps)
driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
time.sleep(5)

driver.terminate_app("com.dbs.kurly.m2")
time.sleep(2)
driver.activate_app("com.dbs.kurly.m2")
time.sleep(5)

handle_kurly_popups(driver, wait_time=10)
time.sleep(2)

print("검색 탭 클릭...")
search_tab = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((AppiumBy.ID, "com.dbs.kurly.m2:id/search"))
)
search_tab.click()

# 1초 후 page source 즉시 저장 (다른 조작 없음)
time.sleep(1)
try:
    src = driver.page_source
    print(f"page_source 길이: {len(src)}")
    with open("search_screen_dump.xml", "w", encoding="utf-8") as f:
        f.write(src)
    print("저장 완료: search_screen_dump.xml (1초 후)")
except Exception as e:
    print(f"1초 후 실패: {e}")

# 3초 후 다시 시도
time.sleep(2)
try:
    src2 = driver.page_source
    print(f"page_source 길이 (3초): {len(src2)}")
    with open("search_screen_dump2.xml", "w", encoding="utf-8") as f:
        f.write(src2)
    print("저장 완료: search_screen_dump2.xml (3초 후)")
except Exception as e:
    print(f"3초 후 실패: {e}")

try:
    driver.quit()
except Exception:
    pass
