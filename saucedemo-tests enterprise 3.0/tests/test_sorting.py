from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


def test_sort_a_to_z(page):
    login = LoginPage(page)
    login.open()
    login.enter_username("standard_user")
    login.enter_password("secret_sauce")
    login.submit()

    inv = InventoryPage(page)
    inv.should_be_here()

    inv.sort_items("az")
    names = inv.get_item_names()
    assert names == sorted(names)
