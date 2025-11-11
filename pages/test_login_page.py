from playwright.sync_api import expect

class LoginPage:
    def __init__(self, page):
        self.page = page
        self.username_input = "#username"
        self.password_input = "#password"
        self.submit_button = "button[type='submit']"
        self.flash = "#flash"
        self.logout_link = "a[href='/logout']"

    def open(self, base_url):
        self.page.goto(base_url)

    def login(self, username, password):
        self.page.fill(self.username_input, username)
        self.page.fill(self.password_input, password)
        self.page.click(self.submit_button)

    def logout(self):
        self.page.click(self.logout_link)

    def assert_login_success(self):
        expect(self.page).to_have_url("https://the-internet.herokuapp.com/secure")

    def assert_login_failure(self):
        expect(self.page.locator(self.flash)).to_contain_text("Your username is invalid!")
