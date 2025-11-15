from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


def test_add_to_cart(page):
    login = LoginPage(page)
    login.open()
    login.enter_username("standard_user")
    login.enter_password("secret_sauce")
    login.submit()

    inv = InventoryPage(page)
    inv.should_be_here()

    inv.add_item("Sauce Labs Backpack")
    assert inv.get_cart_count() == 1

    inv.go_to_cart()
    cart = CartPage(page)
    cart.should_be_here()
    cart.should_contain_item("Sauce Labs Backpack")
