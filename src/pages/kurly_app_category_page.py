from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage, Locator


class KurlyAppCategoryPage(BasePage):
    CATEGORY_TAB_SELECTED: Locator = (
        AppiumBy.XPATH,
        "//android.widget.FrameLayout[@resource-id='com.dbs.kurly.m2:id/category' and @selected='true']",
    )
    CATEGORY_ITEM: Locator = (
        AppiumBy.XPATH,
        "//android.view.View[@clickable='true' and @focusable='true']/android.widget.TextView[string-length(@text) > 0]",
    )

    def has_categories(self) -> bool:
        return self.is_visible(self.CATEGORY_TAB_SELECTED) and self.is_visible(self.CATEGORY_ITEM)
