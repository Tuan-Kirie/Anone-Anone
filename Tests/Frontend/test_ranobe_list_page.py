import time

from .pages.ranobe_list_page import RanobeListPage
from .usable_consts import Consts
from .pages.locators import RanobeListPageLocators
import random


def test_ranobe_detail_page_open(driver):
    page = RanobeListPage(driver, Consts.RANOBE_LIST_URL)
    page.open_page()
    ranobes = driver.find_elements(*RanobeListPageLocators.RANOBE_LIST)
    ranobes[random.randint(0, len(ranobes))].click()
    assert '/details' in driver.current_url, 'Ошибка с переходом на страницу'


def test_search_working(driver):
    """
    test that searched ranobe name == existing first ranobe on searched data
    :param driver:
    :return:
    """
    page = RanobeListPage(driver, Consts.RANOBE_LIST_URL)
    page.open_page()
    ranobe = page.search_ranobe()
    searched_element = page.return_element_after_present(*RanobeListPageLocators.RANOBE_NAMES).text
    assert ranobe == searched_element


def test_search_data_clearing(driver):
    page = RanobeListPage(driver, Consts.RANOBE_LIST_URL)
    first_load_ranobes = page.find_ranobes()
    page.open_page()
    page.search_ranobe()
    assert page.return_element_after_present(*RanobeListPageLocators.RANOBE_NAMES), "Элемент не появился"
    page.clear_search()
    last_load_ranobes = page.find_ranobes()
    assert first_load_ranobes == last_load_ranobes, "Поиск не сбросился"


