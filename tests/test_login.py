from playwright.sync_api import sync_playwright
import os


def test_successful_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()

        page.goto("https://the-internet.herokuapp.com/login")
        page.fill("#username", "tomsmith")
        page.fill("#password", "SuperSecretPassword!")
        page.click("button[type='submit']")

        message = page.locator("#flash").inner_text()
        assert "You logged into a secure area!" in message

        # 📸 Создаём папку screenshots, если её нет
        os.makedirs("screenshots", exist_ok=True)

        # 📸 Сохраняем скриншот
        page.screenshot(path="screenshots/successful_login.png")

        browser.close()
