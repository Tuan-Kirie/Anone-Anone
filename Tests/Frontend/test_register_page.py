import time

import psycopg2

from .pages.register_page import RegisterPage
from .usable_consts import Consts
from .pages.locators import RegisterPageLocators, ProfilePageLocators
import pytest


class TestRegisterPage:
    def test_guest_can_register_and_login(self, driver, delete_registered_user):
        page = RegisterPage(driver, Consts.REGISTER_PAGE_URL)
        page.open_page()
        page.register_test_account()
        assert page.is_element_is_present(*RegisterPageLocators.REGISTER_ACCESS_MSG)
        page.login_test_account_after_register()
        assert page.is_element_is_present(*ProfilePageLocators.PROFILE_BODY)

