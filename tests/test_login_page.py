from playwright.sync_api import sync_playwright


def test_invalid_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()

        # 1. Открываем страницу
        page.goto("https://the-internet.herokuapp.com/login")

        # 2. Вводим неверные данные
        page.fill("#username", "wrong_user")
        page.fill("#password", "wrong_password")

        # 3. Нажимаем кнопку Login
        page.click("button[type='submit']")

        # 4. Проверяем сообщение об ошибке
        message = page.locator("#flash").inner_text()
        assert "Your username is invalid!" in message

        # 5 📸 Сохраняем скриншот
        page.screenshot(path="screenshots/unsuccessful_login.png")


        browser.close()
