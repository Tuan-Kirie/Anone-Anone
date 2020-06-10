from .base_page import BasePage
from .locators import RanobeDetailPageLocators


class RanobeDetailPage(BasePage):

    def like(self):
        like_btn = self.driver.find_element(*RanobeDetailPageLocators.LIKE_BUTTON)
        like_btn.click()

    def add_to_bookmark(self):
        bookmark_btn = self.driver.find_element(*RanobeDetailPageLocators.ADD_TO_BOOKMARK_BTN)
        bookmark_btn.click()

    def add_comment(self):
        comment_input = self.driver.find_element(*RanobeDetailPageLocators.COMMENT_INPUT)
        comment_input.send_keys('This is test comment')
        submit_btn = self.driver.find_element(*RanobeDetailPageLocators.COMMENT_SUBMIT_BTN)
        submit_btn.click()

