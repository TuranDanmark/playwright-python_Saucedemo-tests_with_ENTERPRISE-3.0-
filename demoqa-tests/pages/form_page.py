import logging
from .base_page import BasePage
from faker import Faker
from playwright.sync_api import expect

fake = Faker()

class FormPage(BasePage):
    def __init__(self, page):
        super().__init__(page, "https://demoqa.com/automation-practice-form")
        self.first_name = page.locator("#firstName")
        self.last_name = page.locator("#lastName")
        self.email = page.locator("#userEmail")
        self.gender = page.locator("label[for='gender-radio-1']")
        self.mobile = page.locator("#userNumber")
        self.submit = page.locator("#submit")

    def fill_form(self):
        logging.info("Заполняю форму регистрации...")
        self.first_name.fill(fake.first_name())
        self.last_name.fill(fake.last_name())
        self.email.fill(fake.email())
        self.gender.click()
        self.mobile.fill(fake.msisdn()[:10])
        logging.info("Отправляю форму.")
        self.submit.click()
        expect(self.page.locator(".modal-content")).to_be_visible()
        logging.info("Форма успешно отправлена и модальное окно появилось.")
