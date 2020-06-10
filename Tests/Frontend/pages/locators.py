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
    PROFILE_HIDDEN_MENU_ACTIVE = (By.XPATH, "//*[@id='hiddenMenu'][contains(@style, 'display: flex')]")


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


class RanobeDetailPageLocators:
    LIKE_BUTTON = (By.CSS_SELECTOR, '.like-button')
    GENRES_LINK = (By.CSS_SELECTOR, '.ranobe-genres > span > a')
    AUTHOR_AND_PUBLISHER_LINK = (By.CSS_SELECTOR, '.ranobe-author-publisher > div > span > a')
    READ_BUTTON = (By.CSS_SELECTOR, '.read-button')
    READ_STATUS_MENU_SHOW_BTN = (By.CSS_SELECTOR, '.dropdown-menu > span')
    READ_STATUS_MENU_ADD_PLANNED = (By.CSS_SELECTOR, '.add-to-planned')
    READ_STATUS_MENU_ADD_READE = (By.CSS_SELECTOR, '.add-to-reade')
    READ_STATUS_MENU_ADD_READING = (By.CSS_SELECTOR, '.add-to-reading')
    SHOW_TAGS_BUTTON = (By.CSS_SELECTOR, '.show-tags-b')
    ADD_TO_BOOKMARK_BTN = (By.CSS_SELECTOR, '.add-to-bookmark')
    COMMENT_INPUT = (By.CSS_SELECTOR, '.ck.ck-editor__main > div')
    COMMENT_SUBMIT_BTN = (By.CSS_SELECTOR, '.send-comment-button')


class RegisterPageLocators:
    REGISTER_INPUTS = (By.CSS_SELECTOR, '.register-form > input')
    REGISTER_BTN = (By.CSS_SELECTOR, '.register-form > button')
    REGISTER_ACCESS_MSG = (By.CSS_SELECTOR, '.login-form > .login-message > span')
    LOGIN_FORM_INPUTS = (By.CSS_SELECTOR, '.login-form > input')
    LOGIN_SUBMIT_BTN = (By.CSS_SELECTOR, '.register-form-back .top-button')


class ProfilePageLocators:
    PROFILE_BODY = (By.CSS_SELECTOR, '.profile-container')
