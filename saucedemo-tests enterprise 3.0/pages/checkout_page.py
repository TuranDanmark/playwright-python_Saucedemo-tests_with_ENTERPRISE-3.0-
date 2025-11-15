from utils.enterprise_logger import enterprise_step
from playwright.sync_api import Page, expect


class CheckoutPage:
    def __init__(self, page: Page):
        self.page = page
        self.first = page.locator("#first-name")
        self.last = page.locator("#last-name")
        self.zip = page.locator("#postal-code")
        self.continue_btn = page.locator("[data-test='continue']")
        self.finish_btn = page.locator("[data-test='finish']")
        self.success_msg = page.locator(".complete-header")

    @enterprise_step("Вводим данные покупателя")
    def fill_form(self, first, last, zipcode):
        self.first.fill(first)
        self.last.fill(last)
        self.zip.fill(zipcode)

    @enterprise_step("Нажимаем Continue")
    def proceed(self):
        self.continue_btn.click()

    @enterprise_step("Нажимаем Finish")
    def finish(self):
        self.finish_btn.click()

    @enterprise_step("Проверяем успешное завершение покупки")
    def should_be_completed(self):
        expect(self.success_msg).to_contain_text("Thank you")
