import time
import pytest
from .pages.locators import MainPageLocators
from .pages.main_page import MainPage
from .usable_consts import Consts


# @pytest.mark.skip()
def test_guest_can_go_to_ranobe_list_page(driver):
    page = MainPage(driver, url=Consts.MAIN_PAGE_URL)
    page.open_page()
    page.go_to_ranobe_list_page()
    assert '/ranobe' in page.driver.current_url, "Ошибка с переходом на страницу"


# @pytest.mark.skip()
def test_guest_can_go_to_faq_page(driver):
    page = MainPage(driver, url=Consts.MAIN_PAGE_URL)
    page.open_page()
    page.go_to_faq_page()
    assert '/about' in page.driver.current_url, "Ошибка с переходом на страницу"


# @pytest.mark.skip()
def test_guest_can_see_login_form(driver):
    page = MainPage(driver, url=Consts.MAIN_PAGE_URL)
    page.open_page()
    page.show_login_form()
    assert page.is_element_clickable(*MainPageLocators.LOGIN_FORM), "Ошибка с переходом на страницу"


# @pytest.mark.skip()
def test_guest_can_go_to_news_page(driver):
    page = MainPage(driver, url=Consts.MAIN_PAGE_URL)
    page.open_page()
    page.go_to_news_page()
    assert '/blog' in page.driver.current_url , "Ошибка с переходом на страницу"


@pytest.mark.xfail(reason="ChromeDriver does not correct running ajax(axios) async request, aborting websocket "
                          "connection")
def test_guest_can_login_from_main_page(driver):
    page = MainPage(driver, url=Consts.MAIN_PAGE_URL)
    page.open_page()
    page.show_login_form()
    page.login_test_account()
    time.sleep(30)
    assert '/profile' in page.driver.current_url , "Ошибка Авторизации"
