from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def enter_text(self, locator, value):
        self.wait.until(EC.visibility_of_element_located(locator)).send_keys(value)


class LoginPage(BasePage):
    URL = "https://www.saucedemo.com/"
    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN = (By.ID, "login-button")

    def open(self):
        self.driver.get(self.URL)

    def login(self, username, password):
        self.enter_text(self.USERNAME, username)
        self.enter_text(self.PASSWORD, password)
        self.click(self.LOGIN)
        return InventoryPage(self.driver)


class InventoryPage(BasePage):
    ADD_TO_CART = {
        "Sauce Labs Backpack": (By.ID, "add-to-cart-sauce-labs-backpack"),
        "Sauce Labs Bolt T-Shirt": (By.ID, "add-to-cart-sauce-labs-bolt-t-shirt"),
        "Sauce Labs Onesie": (By.ID, "add-to-cart-sauce-labs-onesie"),
    }
    CART = (By.CLASS_NAME, "shopping_cart_link")

    def add_product(self, name):
        self.click(self.ADD_TO_CART[name])

    def open_cart(self):
        self.click(self.CART)
        return CartPage(self.driver)


class CartPage(BasePage):
    CHECKOUT = (By.ID, "checkout")

    def checkout(self):
        self.click(self.CHECKOUT)
        return CheckoutInformationPage(self.driver)


class CheckoutInformationPage(BasePage):
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE = (By.ID, "continue")

    def submit_information(self, first_name, last_name, postal_code):
        self.enter_text(self.FIRST_NAME, first_name)
        self.enter_text(self.LAST_NAME, last_name)
        self.enter_text(self.POSTAL_CODE, postal_code)
        self.click(self.CONTINUE)
        return CheckoutOverviewPage(self.driver)


class CheckoutOverviewPage(BasePage):
    TOTAL = (By.CLASS_NAME, "summary_total_label")

    def read_total(self):
        label = self.wait.until(EC.visibility_of_element_located(self.TOTAL))
        return label.text.removeprefix("Total:").strip()
