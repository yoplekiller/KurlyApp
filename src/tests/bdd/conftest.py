import pytest
from pages.category_page import CategoryPage
from pages.home_page import HomePage
from pages.search_page import SearchPage


@pytest.fixture
def home_page(driver):
    return HomePage(driver)


@pytest.fixture
def category_page(driver):
    return CategoryPage(driver)


@pytest.fixture
def search_page(driver):
    return SearchPage(driver)
