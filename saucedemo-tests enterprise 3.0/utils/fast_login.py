import json
from pathlib import Path


class FastLogin:
    def __init__(self, browser, cookie_file="cookies.json"):
        self.browser = browser
        self.cookie_file = Path(cookie_file)

    def save_cookies(self, page):
        cookies = page.context.cookies()
        self.cookie_file.write_text(json.dumps(cookies, indent=4))

    def load_cookies(self, context):
        if not self.cookie_file.exists():
            return False
        cookies = json.loads(self.cookie_file.read_text())
        context.add_cookies(cookies)
        return True

    def login_once(self, username, password):
        context = self.browser.new_context()
        page = context.new_page()

        page.goto("https://www.saucedemo.com/")
        page.fill("#user-name", username)
        page.fill("#password", password)
        page.click("#login-button")
        page.wait_for_url("**/inventory.html")

        self.save_cookies(page)
        context.close()

    def fast_login(self, context):
        ok = self.load_cookies(context)
        if not ok:
            return None
        page = context.new_page()
        page.goto("https://www.saucedemo.com/inventory.html")
        return page
