import psycopg2
import pytest
from psycopg2 import connect
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from .usable_consts import Consts


@pytest.fixture(scope='function')
def driver() -> webdriver:
    """
    Main selenium Fixture to initiate ChromeDriver
    :param
    :return: driver instance
    """
    # Added options cause CORS police blocking axios requests from Chromedriver
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


@pytest.fixture(scope='session', autouse=True)
def database():
    con = psycopg2.connect('dbname=anoneanone user=postgres password=301190')
    cursor = con.cursor()
    yield
    delete_registered_user(cursor)
    con.commit()


def delete_registered_user(cursor):
    test_user_username = Consts.TEST_ACCOUNT[0]
    cursor.execute(f"SELECT id FROM auth_user WHERE username='{test_user_username}'")
    test_user_id = cursor.fetchone()[0]
    print(test_user_id)
    cursor.execute(f"DELETE FROM users_profile CASCADE WHERE user_id={test_user_id}")
    cursor.execute(f"DELETE FROM auth_user CASCADE WHERE id={test_user_id}")

    print("ACCOUNT HAS BEEN DELETED")

# database()