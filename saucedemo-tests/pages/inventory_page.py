from playwright.sync_api import expect
from utils.enterprise_logger import enterprise_step


class InventoryPage:
    INVENTORY_ITEM = ".inventory_item"
    ADD_TO_CART_BTN = "[data-test^='add-to-cart']"
    CART_BADGE = ".shopping_cart_badge"
    CART_LINK = ".shopping_cart_link"

    def __init__(self, page):
        self.page = page

    @enterprise_step("Добавляем первый товар в корзину")
    def add_first_item_to_cart(self):
        self.page.wait_for_selector(self.ADD_TO_CART_BTN)
        self.page.locator(self.ADD_TO_CART_BTN).first.click()

    @enterprise_step("Проверяем, что товар добавлен в корзину")
    def assert_cart_counter(self, expected_count="1"):
        expect(self.page.locator(self.CART_BADGE)).to_have_text(expected_count)

    @enterprise_step("Переходим в корзину")
    def open_cart(self):
        self.page.locator(self.CART_LINK).click()
