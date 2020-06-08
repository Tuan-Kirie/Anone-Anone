from .base_page import BasePage
from .locators import MainPageLocators
from ..usable_consts import Consts
from selenium.webdriver.common.action_chains import ActionChains


class MainPage(BasePage):

    def go_to_ranobe_list_page(self):
        ranobe_list_page_link = self.driver.find_element(*MainPageLocators.RANOBE_LIST_PAGE_LINK)
        ranobe_list_page_link.click()

    def go_to_faq_page(self):
        faq_page_link = self.driver.find_element(*MainPageLocators.FAQ_PAGE_LINK)
        faq_page_link.click()

    def show_login_form(self):
        login_form_show_button = self.driver.find_element(*MainPageLocators.OPEN_LOGIN_FORM_LINK)
        action = ActionChains(self.driver)
        action.move_to_element(login_form_show_button)
        action.perform()
        del action

    def go_to_news_page(self):
        news_button = self.driver.find_element(*MainPageLocators.NEWS_PAGE_BTN)
        news_button.click()

    def login_test_account(self):
        self.show_login_form()
        inputs = self.driver.find_elements(*MainPageLocators.LOGIN_FORM_INPUTS)
        [inputs[i].send_keys(Consts.TEST_ACCOUNT[i]) for i in range(len(inputs))]
        button = self.driver.find_element(*MainPageLocators.LOGIN_FORM_LOGIN_BTN)
        button.click()
