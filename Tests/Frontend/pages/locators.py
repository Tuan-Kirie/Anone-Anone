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


class RanobeListPageLocators:
    RANOBE_LIST = (By.CSS_SELECTOR, '.ranobe-container')
    SEARCH_INPUT = (By.CSS_SELECTOR, '.search > form > input')
    SEARCH_CLEAR_BUTTON = (By.CSS_SELECTOR, '#clear-b')
    SEARCH_BUTTON = (By.CSS_SELECTOR, '#search-b')
    RANOBE_NAMES = (By.CSS_SELECTOR, 'span.ranobe-name')
    RANOBE_IMG_CONTAINER = (By.CSS_SELECTOR, '.ranobe-image-cont')
    RANOBE_ADULT_BLURED_IMG = (By.CSS_SELECTOR, '.ran-link > ranobe-img-adult')
    FILTER_ADULT_CHECKBOX = (By.CSS_SELECTOR, '#checkbox')
    GENRES_SHOW_BTN = (By.CSS_SELECTOR, '.genres')
    TAGS_SHOW_BTNS = (By.CSS_SELECTOR, '.tags')
    FILTER_CLEAR_BTN = (By.CSS_SELECTOR, '.clear')
    FILTER_GENRES_LIST = (By.CSS_SELECTOR, '.genres > .meta-list-container > .genres-list')
    FILTER_TAGS_LIST = (By.CSS_SELECTOR, '.tags > .meta-list-container > .genres-list')
