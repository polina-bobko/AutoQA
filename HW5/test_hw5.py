import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@pytest.fixture()
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


# Задание 1: Проверка текста внутри iframe
def test_text_inside_iframe(driver):
    driver.get(
        "https://bonigarcia.dev/selenium-webdriver-java/iframes.html"
    )

    wait = WebDriverWait(driver, 20)

    # Переключаемся в iframe
    wait.until(
        EC.frame_to_be_available_and_switch_to_it(
            (By.ID, "my-iframe")
        )
    )

    target_text = "semper posuere integer et senectus justo curabitur."

    # Ждём, пока нужный текст появится внутри iframe
    wait.until(
        EC.text_to_be_present_in_element(
            (By.TAG_NAME, "body"),
            target_text
        )
    )

    # Проверяем текст
    body = driver.find_element(By.TAG_NAME, "body")

    assert target_text in body.text
    assert body.is_displayed()

    driver.switch_to.default_content()

# Задание 2: Drag & Drop изображения в корзину
def test_drag_photo_to_trash(driver):
    driver.get(
        "https://www.globalsqa.com/demo-site/draganddrop/"
    )

    wait = WebDriverWait(driver, 15)

    # Закрываем cookie-баннер, если он появился
    try:
        cookie_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.fc-cta-consent")
            )
        )
        cookie_button.click()
    except TimeoutException:
        pass

    # Переключаемся в iframe
    wait.until(
        EC.frame_to_be_available_and_switch_to_it(
            (By.CSS_SELECTOR, "iframe.demo-frame")
        )
    )

    # Находим галерею и корзину
    gallery = driver.find_element(By.ID, "gallery")
    trash = driver.find_element(By.ID, "trash")

    # Проверяем начальное количество фотографий
    assert len(gallery.find_elements(By.TAG_NAME, "li")) == 4
    assert len(trash.find_elements(By.TAG_NAME, "li")) == 0

    # Находим первую фотографию
    first_photo = gallery.find_element(By.TAG_NAME, "li")

    # Перетаскиваем в корзину
    ActionChains(driver) \
        .click_and_hold(first_photo) \
        .move_to_element(trash) \
        .move_by_offset(5, 5) \
        .pause(0.5) \
        .release() \
        .perform()

    # Ждём появления фотографии в корзине
    wait.until(
        lambda d: len(
            trash.find_elements(By.TAG_NAME, "li")
        ) == 1
    )

    # Проверяем результат
    assert len(gallery.find_elements(By.TAG_NAME, "li")) == 3
    assert len(trash.find_elements(By.TAG_NAME, "li")) == 1
