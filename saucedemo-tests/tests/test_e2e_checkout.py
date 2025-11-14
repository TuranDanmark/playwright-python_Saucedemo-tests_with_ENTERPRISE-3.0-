import allure
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


@allure.feature("E2E Checkout")
@allure.story("Полный процесс покупки")
@allure.severity(allure.severity_level.CRITICAL)
def test_e2e_full_checkout(page):
    login = LoginPage(page)
    inventory = InventoryPage(page)
    cart = CartPage(page)
    checkout = CheckoutPage(page)

    # --- Login ---
    login.goto()
    login.login("standard_user", "secret_sauce")
    login.assert_login_success()

    # --- Add to cart ---
    inventory.add_first_item_to_cart()
    inventory.assert_cart_counter("1")
    inventory.open_cart()

    # --- Cart ---
    cart.assert_cart_not_empty()
    cart.go_to_checkout()

    # --- Checkout ---
    checkout.fill_user_info("Turan", "QA", "2200")
    checkout.finish_checkout()
    checkout.assert_order_complete()
