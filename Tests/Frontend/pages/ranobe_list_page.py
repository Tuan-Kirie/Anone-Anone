from .base_page import BasePage
from .locators import RanobeListPageLocators
from ..usable_consts import Consts
import random


class RanobeListPage(BasePage):

    def find_ranobes(self):
        ranobes = self.driver.find_elements(*RanobeListPageLocators.RANOBE_NAMES)
        return ranobes

    def search_ranobe(self):
        ranobe_names = self.find_ranobes()
        search_input = self.driver.find_element(*RanobeListPageLocators.SEARCH_INPUT)
        rnd_name = ranobe_names[random.randint(0, len(ranobe_names))].text
        search_input.send_keys(rnd_name)
        submit_btn = self.driver.find_element(*RanobeListPageLocators.SEARCH_BUTTON)
        submit_btn.click()
        return rnd_name

    def clear_search(self):
        clear_btn = self.driver.find_element(*RanobeListPageLocators.SEARCH_CLEAR_BUTTON)
        clear_btn.click()
