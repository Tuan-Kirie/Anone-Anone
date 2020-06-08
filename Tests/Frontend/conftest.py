import pytest
from selenium import webdriver


@pytest.fixture(scope='function')
def driver():
    """
    Main selenium Fixture to initiate ChromeDriver
    :param
    :return: driver instance
    """
    driver = webdriver.Chrome()
    print('Chrome initiated')
    yield driver
    driver.quit()
