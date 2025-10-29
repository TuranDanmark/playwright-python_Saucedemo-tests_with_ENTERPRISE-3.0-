from playwright.sync_api import sync_playwright
import os

def test_registration_form():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=400)
        page = browser.new_page()
        os.makedirs("screenshots", exist_ok=True)

        # 1. Открываем страницу
        page.goto("https://demoqa.com/automation-practice-form")

        # 2. Заполняем поля
        page.fill("#firstName", "Alex")
        page.fill("#lastName", "Tester")
        page.fill("#userEmail", "alex@example.com")
        page.click("label[for='gender-radio-1']")  # Male
        page.fill("#userNumber", "1234567890")

        # 3. Отправляем форму
        page.click("#submit")

        # 4. Проверяем, что открылась таблица с подтверждением
        modal_title = page.locator("#example-modal-sizes-title-lg").inner_text()
        assert "Thanks for submitting the form" in modal_title

        # 5. Проверяем, что в таблице есть имя
        table_text = page.locator(".table-responsive").inner_text()
        assert "Alex Tester" in table_text

        # 6. Скриншот результата
        page.screenshot(path="screenshots/form_success.png")

        browser.close()