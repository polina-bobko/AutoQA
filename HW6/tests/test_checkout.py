from selenium import webdriver
from pages.sauce_demo import LoginPage


def test_checkout_total():
    options = webdriver.ChromeOptions()

    with webdriver.Chrome(options=options) as browser:
        login_page = LoginPage(browser)
        login_page.open()
        inventory = login_page.login("standard_user", "secret_sauce")

        inventory.add_product("Sauce Labs Backpack")
        inventory.add_product("Sauce Labs Bolt T-Shirt")
        inventory.add_product("Sauce Labs Onesie")

        cart = inventory.open_cart()
        checkout = cart.checkout()
        overview = checkout.submit_information("Polina", "Bobko", "10115")
        total = overview.read_total()

    assert total == "$58.29"
