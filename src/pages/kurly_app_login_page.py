from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage, Locator


class KurlyAppLoginPage(BasePage):
    EMAIL_INPUT: Locator = (AppiumBy.ID, "com.dbs.kurly.m2:id/etId")
    PASSWORD_INPUT: Locator = (AppiumBy.ID, "com.dbs.kurly.m2:id/etPassword")
    LOGIN_BUTTON: Locator = (AppiumBy.ID, "com.dbs.kurly.m2:id/loginButton")


    def login(self, user_id: str, password: str) -> None:
        self.input_text(self.EMAIL_INPUT, user_id)
        self.input_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        

    def is_login_screen(self) -> bool:
        return self.is_visible(self.LOGIN_BUTTON)
