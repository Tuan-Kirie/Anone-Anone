import time

from .pages.register_page import RegisterPage
from .usable_consts import Consts
from .pages.locators import RegisterPageLocators, MainPageLocators


class TestRegisterPage:
    def test_guest_can_register_and_login(self, driver):
        page = RegisterPage(driver, Consts.REGISTER_PAGE_URL)
        page.open_page()
        page.register_test_account()
        time.sleep(40)
        assert page.is_element_is_present(*RegisterPageLocators.REGISTER_ACCESS_MSG)
        page.login_test_account_after_register()
        assert page.is_element_is_present(*MainPageLocators.PROFILE_HIDDEN_MENU_ACTIVE)
