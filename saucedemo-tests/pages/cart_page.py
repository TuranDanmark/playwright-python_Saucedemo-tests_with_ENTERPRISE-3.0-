from playwright.sync_api import expect
from utils.enterprise_logger import enterprise_step


class CartPage:
    CART_ITEM = ".cart_item"
    CHECKOUT_BTN = "[data-test='checkout']"

    def __init__(self, page):
        self.page = page

    @enterprise_step("Проверяем, что в корзине есть товар")
    def assert_cart_not_empty(self):
        expect(self.page.locator(self.CART_ITEM)).to_be_visible()

    @enterprise_step("Нажимаем Checkout")
    def go_to_checkout(self):
        self.page.locator(self.CHECKOUT_BTN).click()
