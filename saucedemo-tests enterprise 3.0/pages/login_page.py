from utils.enterprise_logger import enterprise_step
from playwright.sync_api import Page, expect


class LoginPage:
    URL = "https://www.saucedemo.com/"

    def __init__(self, page: Page):
        self.page = page
        self.username = page.locator("#user-name")
        self.password = page.locator("#password")
        self.login_btn = page.locator("#login-button")
        self.error_msg = page.locator("[data-test='error']")

    @enterprise_step("Открываем страницу логина")
    def open(self):
        self.page.goto(self.URL)

    @enterprise_step("Вводим логин: {1}")
    def enter_username(self, username):
        self.username.fill(username)

    @enterprise_step("Вводим пароль")
    def enter_password(self, password):
        self.password.fill(password)

    @enterprise_step("Нажимаем Login")
    def submit(self):
        self.login_btn.click()

    @enterprise_step("Проверяем успешный вход")
    def should_be_logged_in(self):
        expect(self.page).to_have_url("**/inventory.html", timeout=10_000)

    @enterprise_step("Проверяем ошибку: {1}")
    def should_have_error(self, msg):
        expect(self.error_msg).to_contain_text(msg)
