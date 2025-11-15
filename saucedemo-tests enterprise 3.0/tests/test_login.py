from pages.login_page import LoginPage


def test_login_success(page):
    login = LoginPage(page)
    login.open()
    login.enter_username("standard_user")
    login.enter_password("secret_sauce")
    login.submit()
    login.should_be_logged_in()


def test_login_fail(page):
    login = LoginPage(page)
    login.open()
    login.enter_username("wrong")
    login.enter_password("wrong")
    login.submit()
    login.should_have_error("Username and password do not match")
