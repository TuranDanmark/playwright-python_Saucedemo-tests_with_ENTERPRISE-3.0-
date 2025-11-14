from playwright.sync_api import expect
from utils.enterprise_logger import enterprise_step


class LoginPage:
    URL = "https://www.saucedemo.com/"
    USERNAME = "[data-test='username']"
    PASSWORD = "[data-test='password']"
    LOGIN_BTN = "[data-test='login-button']"

    def __init__(self, page):
        self.page = page

    @enterprise_step("Открываем страницу логина")
    def goto(self):
        self.page.goto(self.URL)
        self.page.wait_for_selector(self.USERNAME, timeout=15000)

    @enterprise_step("Вводим логин и пароль, кликаем 'Login'")
    def login(self, username, password):
        username_input = self.page.locator(self.USERNAME)
        password_input = self.page.locator(self.PASSWORD)
        login_button = self.page.locator(self.LOGIN_BTN)

        username_input.wait_for(state="visible", timeout=10000)
        username_input.click()
        username_input.clear()
        username_input.fill(username)

        password_input.wait_for(state="visible", timeout=10000)
        password_input.click()
        password_input.clear()
        password_input.fill(password)

        login_button.wait_for(state="attached", timeout=5000)
        login_button.click()

    @enterprise_step("Проверяем успешный вход")
    def assert_login_success(self):
        self.page.wait_for_load_state("networkidle")
        expect(self.page).to_have_url("https://www.saucedemo.com/inventory.html", timeout=15000)
        expect(self.page.locator(".inventory_list")).to_be_visible()

    @enterprise_step("Проверяем ошибку авторизации")
    def assert_login_failed(self):
        error = self.page.locator("[data-test='error']")
        expect(error).to_be_visible(timeout=5000)
