import psycopg2
import pytest
from psycopg2 import connect
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from .usable_consts import Consts


class Database:
    """
    Create postgress database instance to delete registered account
    :return:
    """

    def __init__(self):
        self.con = psycopg2.connect('dbname=anoneanone user=postgres password=301190')
        self.cursor = self.con.cursor()

    def delete_registered_user(self, username):
        test_user_username = username
        self.cursor.execute(f"SELECT id FROM auth_user WHERE username='{test_user_username}'")
        test_user_id = self.cursor.fetchone()[0]
        self.cursor.execute(f"DELETE FROM users_profile CASCADE WHERE user_id={test_user_id}")
        self.con.commit()
        self.cursor.execute(f"DELETE FROM auth_user CASCADE WHERE id={test_user_id}")
        self.con.commit()
        print("ACCOUNT HAS BEEN DELETED")

    def create_test_account(self):
        self.cursor.execute("""INSERT INTO auth_user (username, password, email, is_superuser, first_name, last_name, is_staff, is_active, date_joined)
                       VALUES ('main_test_account', 'pbkdf2_sha256$180000$UOy3H6XECTLD$ukrsFGgOO4ZGywx/JJKBmt9/x2d6OOvK5ZphfDlKTl0=', 'main_test_account_p@ss.ff', FALSE, 'main_test_account_p',
                       'main_test_account_p', FALSE, TRUE, '1999-01-08');
                       """)
        self.con.commit()
        self.cursor.execute("SELECT id FROM auth_user WHERE username='main_test_account'")
        user_id = self.cursor.fetchone()[0]
        self.cursor.execute(
            f"INSERT INTO users_profile (profile_img, user_id) VALUES ('media/profile/default.jpg', {user_id})")
        self.con.commit()


@pytest.fixture(scope='function')
def driver() -> webdriver:
    """
    Main selenium Fixture to initiate ChromeDriver
    :param
    :return: driver instance
    """
    # Added options cause CORS police blocking axios requests to backend api
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
def init_accounts():
    db = Database()
    db.create_test_account()
    yield
    db.delete_registered_user('main_test_account')


@pytest.fixture()
def delete_registered_user():
    db = Database()
    yield
    db.delete_registered_user(Consts.TEST_ACCOUNT[0])
