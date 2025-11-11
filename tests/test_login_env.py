import pytest
from pages.test_login_page import LoginPage

def test_successful_login(page_with_video, base_url, credentials):
    login_page = LoginPage(page_with_video)
    login_page.open(base_url)
    login_page.login(credentials["username"], credentials["password"])
    login_page.assert_login_success()

def test_unsuccessful_login(page_with_video, base_url):
    login_page = LoginPage(page_with_video)
    login_page.open(base_url)
    login_page.login("wrong_user", "bad_password")
    login_page.assert_login_failure()
