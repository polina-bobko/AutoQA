from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import pytest


@pytest.fixture
def driver():
    driver = webdriver.Firefox()
    driver.maximize_window()
    yield driver
    driver.quit()

def test_payment_methods(driver):
    driver.get("https://itcareerhub.de/ru")
    sleep(2)
    payment_methods_btn = driver.find_element(By.CSS_SELECTOR, "#molecule-176285426165558590 > div.t396__elem.tn-elem.t396__elem-flex.tn-elem__1921710463176285426166311940 > a")
    payment_methods_btn.click()
    sleep(2)
    driver.save_screenshot("./HW2/itch_payment_methods.png")