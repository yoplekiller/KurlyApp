"""검색 페이지 page source 덤프 - 긴 대기"""
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

# 각 초마다 page source 저장
for wait_sec in [1, 3, 5, 8, 10]:
    time.sleep(1 if wait_sec == 1 else 2)
    try:
        src = driver.page_source
        fname = f"search_dump_{wait_sec}s.xml"
        with open(fname, "w", encoding="utf-8") as f:
            f.write(src)
        # navigation bar 확인
        import xml.etree.ElementTree as ET
        root = ET.fromstring(src)
        home_active = False
        search_active = False
        for elem in root.iter():
            rid = elem.get("resource-id", "")
            sel = elem.get("selected", "")
            if rid == "com.dbs.kurly.m2:id/home" and sel == "true":
                home_active = True
            if rid == "com.dbs.kurly.m2:id/search" and sel == "true":
                search_active = True
        total_elems = sum(1 for _ in root.iter())
        print(f"[{wait_sec}s] len={len(src)} elems={total_elems} home_active={home_active} search_active={search_active}")
    except Exception as e:
        print(f"[{wait_sec}s] error: {e}")

try:
    driver.quit()
except Exception:
    pass
