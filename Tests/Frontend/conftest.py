import pytest
from psycopg2 import connect
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope='function')
def driver() -> webdriver:
    """
    Main selenium Fixture to initiate ChromeDriver
    :param
    :return: driver instance
    """
    chrome_options = Options()
    executable_path = 'C:\chromedriver\chromedriver.exe'
    chrome_options.add_argument("--test-type")
    chrome_options.add_argument("--user-data-dir=D:\\chrome")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument("--allow-cross-origin-auth-prompt")
    chrome_options.add_argument("-–allow-file-access-from-files")
    chrome_options.add_argument('--disable-site-isolation-trials')
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=executable_path)
    print('Chrome initiated')
    yield driver

    driver.quit()


