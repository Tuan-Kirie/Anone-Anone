from selenium.webdriver.common.by import By


class MainPageLocators:
    RANOBE_LIST_PAGE_LINK = (By.CSS_SELECTOR, '#ranobe-link')
    FAQ_PAGE_LINK = (By.CSS_SELECTOR, '#question-link')
    OPEN_LOGIN_FORM_LINK = (By.CSS_SELECTOR, '#login-link')
    LOGIN_FORM = (By.CSS_SELECTOR, '.login-form')
    NEWS_PAGE_BTN = (By.CSS_SELECTOR, '.read-btn')
    LOGIN_FORM_INPUTS = (By.CSS_SELECTOR, '.login-form > input')
    LOGIN_FORM_LOGIN_BTN = (By.CSS_SELECTOR, '#login-btn')
    LOGIN_FORM_REGISTER_BTN = (By.CSS_SELECTOR, '#register-btn')
