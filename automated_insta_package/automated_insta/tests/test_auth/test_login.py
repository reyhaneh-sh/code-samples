import unittest

from automated_insta.auth.decorators import is_logged_in
from automated_insta.auth.login import login_by_username, login_by_cookie
from automated_insta.constants.exceptions.auth import (INVALID_COOKIE_DOMAIN_EXCEPTION_MESSAGE,
                                                       INVALID_COOKIE_EXCEPTION_MESSAGE)
from automated_insta.exceptions.auth import LoginFormNotFoundException, LoginFailedException
from automated_insta.exceptions.driver import IrrelevantDomainException
from automated_insta.tests import TestResult, _load_sessionid_cookie
from automated_insta.tests.constants.auth import WRONG_PASSWORD
from automated_insta.tests.constants.core import (URL_WITH_IRRELEVANT_DOMAIN,
                                                  PAGE_NOT_FOUND,
                                                  INVALID_COOKIE_DOMAIN,
                                                  INVALID_COOKIE_VALUE)
from automated_insta.tests.environment import environment
from . import _add_csrf_cookie


class LoginByUsername(unittest.TestCase):
    webdriver = None

    @classmethod
    def setUpClass(cls):
        cls.webdriver = TestResult.WEBDRIVER
        cls.username = environment.INSTAGRAM_USERNAME
        cls.password = environment.INSTAGRAM_PASSWORD
        cls.timeout = 3

    def test_irrelevant_domain_exception(self):
        self.webdriver.get(URL_WITH_IRRELEVANT_DOMAIN)
        self.assertRaises(IrrelevantDomainException, login_by_username, self.webdriver, self.username, self.password)

    def test_login_form_not_found_exception(self):
        self.webdriver.get(PAGE_NOT_FOUND)
        self.assertRaises(LoginFormNotFoundException, login_by_username, self.webdriver, self.username, self.password)

    def test_login_failed_exception(self):
        self.webdriver.get_login_page()
        self.assertRaises(LoginFailedException, login_by_username,
                          self.webdriver, self.username, WRONG_PASSWORD, self.timeout)

    def test_successful_login(self):
        self.webdriver.get_login_page()
        if not self.webdriver.get_cookie('csrftoken'):
            _add_csrf_cookie(self.webdriver)
        cookies = login_by_username(self.webdriver, self.username, self.password)
        self.assertIsNotNone(cookies)

    def test_is_logged_in_True(self):
        self.webdriver.get_login_page()
        self.webdriver.add_cookie({'name': 'sessionid', 'value': 'fake_value_to_simulate_user_is_logged_in'})
        self.assertTrue(is_logged_in(self.webdriver, timeout=self.timeout))

    def test_is_logged_in_False(self):
        self.webdriver.get_login_page()
        self.assertFalse(is_logged_in(self.webdriver, timeout=self.timeout))


class LoginByCookies(unittest.TestCase):
    webdriver = None

    @classmethod
    def setUpClass(cls):
        cls.webdriver = TestResult.WEBDRIVER
        cls.sessionid_cookie = _load_sessionid_cookie(cls.webdriver)

    def test_irrelevant_domain_exception(self):
        self.webdriver.get(URL_WITH_IRRELEVANT_DOMAIN)
        self.assertRaises(IrrelevantDomainException, login_by_cookie, self.webdriver, self.sessionid_cookie)

    def test_successful_login(self):
        self.webdriver.get_login_page()
        cookies = login_by_cookie(self.webdriver, self.sessionid_cookie)
        self.assertIsNotNone(cookies)

    def test_irrelevant_cookie_domain_exception(self):
        self.webdriver.get_login_page()
        irrelevant_domain_cookie = self.__get_irrelevant_domain_cookie()
        with self.assertRaises(LoginFailedException) as e:
            login_by_cookie(self.webdriver, irrelevant_domain_cookie)
        self.assertEqual(INVALID_COOKIE_DOMAIN_EXCEPTION_MESSAGE, str(e.exception))

    def test_invalid_cookie_exception(self):
        self.webdriver.get_login_page()
        invalid_cookie_cookie = self.__get_invalid_cookie()
        with self.assertRaises(LoginFailedException) as e:
            login_by_cookie(self.webdriver, invalid_cookie_cookie)
        self.assertEqual(INVALID_COOKIE_EXCEPTION_MESSAGE, str(e.exception))

    def __get_irrelevant_domain_cookie(self):
        cookie = self.sessionid_cookie.copy()
        cookie['domain'] = INVALID_COOKIE_DOMAIN
        return cookie

    #
    def __get_invalid_cookie(self):
        cookie = self.sessionid_cookie.copy()
        cookie['value'] = INVALID_COOKIE_VALUE
        return cookie
