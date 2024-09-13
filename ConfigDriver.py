import pytest
from selenium import webdriver

# define the driver for webdriver to open the website that it will tested and for use it in the test function
@pytest.fixture
def driver():
    driver = webdriver.Chrome(executable_path='C:\chromedriver-win64\chromedriver.exe')
    driver.maximize_window()
    yield driver
    driver.quit()
