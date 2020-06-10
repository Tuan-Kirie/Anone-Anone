from .base_page import BasePage
from .locators import RegisterPageLocators



class RegisterPage(BasePage):

    def register_test_account(self):
        inputs = self.driver.find_elements(*RegisterPageLocators.REGISTER_INPUTS)
        inputs[0].send_keys('test_user_1')
        inputs[1].send_keys('test_user_1')
        inputs[2].send_keys('test_user_1')
        inputs[3].send_keys('test_user_1@gmail.com')
        submit_btn = self.driver.find_element(*RegisterPageLocators.REGISTER_BTN)
        submit_btn.click()

    def login_test_account_after_register(self):
        login_submit = self.return_element_after_present(*RegisterPageLocators.LOGIN_SUBMIT_BTN)
        login_submit.click()


