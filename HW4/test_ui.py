import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@pytest.fixture()
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


# Задание 1: Проверка изменения текста кнопки
def test_itch_in_blue_button(driver):
    driver.get("http://uitestingplayground.com/textinput")
    wait = WebDriverWait(driver, 10)

    # Ввод текста ITCH
    input_field = wait.until(
        EC.visibility_of_element_located(
            (By.ID, "newButtonName")
        )
    )
    input_field.send_keys("ITCH")

    # Клик по синей кнопке
    blue_button = driver.find_element(By.ID, "updatingButton")
    blue_button.click()

    # Ожидание изменения текста кнопки
    wait.until(
        EC.text_to_be_present_in_element(
            (By.ID, "updatingButton"), "ITCH"
        )
    )

    # Проверка текста
    assert blue_button.text == "ITCH", (
        "Текст кнопки не изменился на ITCH"
    )


# Задание 2: Проверка загрузки изображений
def test_wait_all_images(driver):
    driver.get(
        "https://bonigarcia.dev/selenium-webdriver-java/loading-images.html"
    )

    wait = WebDriverWait(driver, 20)

    # Ждём, пока появятся все 4 изображения
    wait.until(
        lambda dr: sum(
            image.is_displayed()
            for image in dr.find_elements(
                By.CSS_SELECTOR, "#image-container > img"
            )
        ) == 4
    )

    # Находим третье изображение
    third_image = driver.find_element(
        By.CSS_SELECTOR,
        "#image-container > img:nth-child(3)"
    )

    # Проверяем alt
    assert third_image.get_attribute("alt") == "award"
