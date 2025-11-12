import logging
from .base_page import BasePage
from playwright.sync_api import expect

class TablesPage(BasePage):
    def __init__(self, page):
        super().__init__(page, "https://demoqa.com/webtables")
        self.add_button = page.locator("#addNewRecordButton")
        self.first_name = page.locator("#firstName")
        self.last_name = page.locator("#lastName")
        self.email = page.locator("#userEmail")
        self.age = page.locator("#age")
        self.salary = page.locator("#salary")
        self.department = page.locator("#department")
        self.submit = page.locator("#submit")
        self.table = page.locator(".rt-tbody")

    def add_user(self, first, last, email, age, salary, dept):
        logging.info(f"Добавляю нового пользователя: {first} {last}, {email}")
        self.add_button.click()
        self.first_name.fill(first)
        self.last_name.fill(last)
        self.email.fill(email)
        self.age.fill(str(age))
        self.salary.fill(str(salary))
        self.department.fill(dept)
        self.submit.click()
        logging.info("Пользователь успешно добавлен в таблицу.")

    def verify_user(self, email):
        logging.info(f"Проверяю, что пользователь с email {email} отображается в таблице.")
        expect(self.table).to_contain_text(email)
