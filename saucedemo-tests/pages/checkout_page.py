from playwright.sync_api import expect
from utils.enterprise_logger import enterprise_step


class CheckoutPage:
    FIRSTNAME = "[data-test='firstName']"
    LASTNAME = "[data-test='lastName']"
    POSTAL = "[data-test='postalCode']"
    CONTINUE_BTN = "[data-test='continue']"
    FINISH_BTN = "[data-test='finish']"
    COMPLETE_HEADER = ".complete-header"

    def __init__(self, page):
        self.page = page

    @enterprise_step("Заполняем форму покупателя")
    def fill_user_info(self, first_name, last_name, postal):
        self.page.fill(self.FIRSTNAME, first_name)
        self.page.fill(self.LASTNAME, last_name)
        self.page.fill(self.POSTAL, postal)
        self.page.locator(self.CONTINUE_BTN).click()

    @enterprise_step("Завершаем покупку")
    def finish_checkout(self):
        self.page.locator(self.FINISH_BTN).click()

    @enterprise_step("Проверяем успешное завершение покупки")
    def assert_order_complete(self):
        expect(self.page.locator(self.COMPLETE_HEADER)).to_have_text("Thank you for your order!")
