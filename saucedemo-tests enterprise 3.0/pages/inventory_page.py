from playwright.sync_api import Page, expect
from utils.enterprise_logger import enterprise_step


class InventoryPage:
    URL = "https://www.saucedemo.com/inventory.html"

    def __init__(self, page: Page):
        self.page = page
        self.sort_select = page.locator("[data-test='product_sort_container']")
        self.cart_btn = page.locator("#shopping_cart_container")
        self.cart_badge = page.locator(".shopping_cart_badge")

    @enterprise_step("Проверяем URL Inventory")
    def should_be_here(self):
        expect(self.page).to_have_url(self.URL)

    @enterprise_step("Сортируем: {1}")
    def sort_items(self, criteria):
        self.sort_select.wait_for(state="visible", timeout=10_000)
        self.sort_select.select_option(criteria)

    @enterprise_step("Получаем имена товаров")
    def get_item_names(self):
        return self.page.locator(".inventory_item_name").all_inner_texts()

    @enterprise_step("Получаем цены товаров")
    def get_item_prices(self):
        prices = self.page.locator(".inventory_item_price").all_inner_texts()
        return [float(p.replace("$", "")) for p in prices]

    @enterprise_step("Добавляем товар в корзину: {1}")
    def add_item(self, name):
        locator = self.page.locator(".inventory_item").filter(
            has=self.page.locator(".inventory_item_name", has_text=name)
        )
        locator.locator("button").click()

    @enterprise_step("Переходим в корзину")
    def go_to_cart(self):
        self.cart_btn.click()

    @enterprise_step("Получаем количество в корзине")
    def get_cart_count(self):
        if self.cart_badge.count() == 0:
            return 0
        return int(self.cart_badge.inner_text())
