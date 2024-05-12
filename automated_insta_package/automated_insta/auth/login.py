from typing import List, Optional, Dict

from selenium.common import InvalidCookieDomainException

from automated_insta.auth.alerts import Alert
from automated_insta.auth.decorators import login_form_exist, is_logged_in
from automated_insta.constants.exceptions.auth import (INVALID_COOKIE_DOMAIN_EXCEPTION_MESSAGE,
                                                       INVALID_COOKIE_EXCEPTION_MESSAGE)
from automated_insta.exceptions.auth import LoginFailedException
from automated_insta.locators.auth.login_by_username import LoginByUsernameLocators as Locators
from automated_insta.utils.elements import Elements
from automated_insta.webdriver.decorators import relevant_domain_required
from automated_insta.webdriver.webdriver import WebDriver


@relevant_domain_required
@login_form_exist
def login_by_username(webdriver: WebDriver, username: str, password: str, timeout: Optional[float] = 30) -> List[dict]:
    """
    Fills the login form with the given values and login.
    Returns the cookies if logging in was successful, else throws 'LoginFailedException'

    :param webdriver:
    :param username: Instagram username, phone number or email
    :param password: Instagram password
    :param timeout: Number of seconds to wait for checking if the user has logged in successfully
    :return: The cookies of webdriver
    """
    elem_username_field = Elements.get_element(webdriver, Locators.USERNAME_FIELD)
    elem_password_field = Elements.get_element(webdriver, Locators.PASSWORD_FIELD)
    elem_login_btn = Elements.get_element(webdriver, Locators.LOGIN_BTN)

    Elements.send_keys(elem_username_field, username)
    Elements.send_keys(elem_password_field, password)
    elem_login_btn.click()

    if not is_logged_in(webdriver, timeout=timeout):
        raise LoginFailedException
    return webdriver.get_cookies()


@relevant_domain_required
def get_login_failed_alert(webdriver: WebDriver) -> Alert:
    """
    Returns Alert object based on what alert message Instagram shows.
    Throws ElementNotFoundException if there is no alert element.
    """
    elem_alert = Elements.get_element(webdriver, Locators.ALERT)
    return Alert(elem_alert.text)


@relevant_domain_required
def login_by_cookie(webdriver: WebDriver, sessionid_cookie: Dict, timeout: Optional[float] = 2) -> List[dict]:
    """

    :param webdriver:
    :param sessionid_cookie: A valid cookie associated with Instagram domain
    :param timeout: Number of seconds to wait for checking if the user has logged in successfully
    :return: The cookies of webdriver
    """
    try:
        webdriver.add_cookie(sessionid_cookie)
    except InvalidCookieDomainException:
        raise LoginFailedException(INVALID_COOKIE_DOMAIN_EXCEPTION_MESSAGE)

    webdriver.refresh()  # To ensure proper recognition of the updated cookie.

    if not is_logged_in(webdriver, timeout=timeout):
        raise LoginFailedException(INVALID_COOKIE_EXCEPTION_MESSAGE)
    return webdriver.get_cookies()
