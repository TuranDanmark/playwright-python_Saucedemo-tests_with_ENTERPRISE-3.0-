from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


def test_checkout(page):
    login = LoginPage(page)
    login.open()
    login.enter_username("standard_user")
    login.enter_password("secret_sauce")
    login.submit()

    inv = InventoryPage(page)
    inv.add_item("Sauce Labs Backpack")
    inv.go_to_cart()

    cart = CartPage(page)
    cart.go_to_checkout()

    checkout = CheckoutPage(page)
    checkout.fill_form("Turan", "Denmark", "19300")
    checkout.proceed()
    checkout.finish()
    checkout.should_be_completed()
