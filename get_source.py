from appium import webdriver
from appium.options.android import UiAutomator2Options
import time

caps = {
    "platformName": "Android",
    "automationName": "UiAutomator2",
    "deviceName": "R59T304FH1B",
    "udid": "adb-R59T304FH1B-07Djog._adb-tls-connect._tcp",
    "appPackage": "com.dbs.kurly.m2",
    "noReset": True,
    "forceAppLaunch": False,
    "newCommandTimeout": 60,
}

options = UiAutomator2Options().load_capabilities(caps)
driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
time.sleep(3)

with open("native_source.xml", "w", encoding="utf-8") as f:
    f.write(driver.page_source)

print("저장 완료: native_source.xml")
driver.quit()
