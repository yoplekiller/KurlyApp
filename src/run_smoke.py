from appium import webdriver
from appium.options.android import UiAutomator2Options
from config.app_config import AppConfig
from pages.kurly_app_home_page import KurlyAppHomePage
from utils.popup_handler import handle_kurly_popups


def run() -> None:
    options = UiAutomator2Options().load_capabilities(AppConfig.get_capabilities())
    driver = webdriver.Remote(AppConfig.APPIUM_SERVER_URL, options=options)

    try:
        handle_kurly_popups(driver, wait_time=AppConfig.POPUP_WAIT)
        home_page = KurlyAppHomePage(driver)
        print(f"Kurly app loaded: {home_page.is_loaded()}")
    finally:
        driver.quit()


if __name__ == "__main__":
    run()
