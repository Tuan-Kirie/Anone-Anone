from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


class BasePage:
    def __init__(self, driver: webdriver.Chrome, url, timeout=4):
        self.driver = driver
        self.url = url
        self.timeout = timeout

    def open_page(self):
        self.driver.get(self.url)

    def is_element_is_present(self, selector, locator):
        try:
            WebDriverWait(self.driver, self.timeout).until(
                expected_conditions.presence_of_element_located((selector, locator)))
        except TimeoutException:
            return False
        return True

    def is_element_clickable(self, selector, locator):
        try:
            WebDriverWait(self.driver, self.timeout).until(
                expected_conditions.element_to_be_clickable((selector, locator)))
        except TimeoutException:
            return False
        return True

    def return_element_after_present(self, selector, locator):
        try:
            WebDriverWait(self.driver, 4).until(expected_conditions.presence_of_element_located((selector, locator)))
            return self.driver.find_element(selector, locator)
        except TimeoutException:
            return False


