from utils.enterprise_logger import enterprise_step
from playwright.sync_api import Page, expect


class CartPage:
    URL = "https://www.saucedemo.com/cart.html"

    def __init__(self, page: Page):
        self.page = page
        self.checkout_btn = page.locator("[data-test='checkout']")
        self.items = page.locator(".cart_item")

    @enterprise_step("Проверяем загрузку корзины")
    def should_be_here(self):
        expect(self.page).to_have_url(self.URL)

    @enterprise_step("Проверяем, что товар добавлен: {1}")
    def should_contain_item(self, name):
        expect(self.page.locator(".inventory_item_name")).to_contain_text(name)

    @enterprise_step("Переходим к оформлению заказа")
    def go_to_checkout(self):
        self.checkout_btn.click()
