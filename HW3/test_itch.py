import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture()
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://itcareerhub.de/ru")
    yield driver
    driver.quit()


def test_is_display(driver):
    wait = WebDriverWait(driver, 10)

    # Проверка логотипа
    logo = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '[alt="IT Career Hub"]')
        )
    )
    assert logo.is_displayed()

    # Проверка пунктов меню
    menu_items = {
        "Программы": '[href="#submenu:more"] span',
        "Способы оплаты": '[href="#rec1921734713"] span',
        "О нас": '[href="#submenu:more2"] span',
        "Отзывы": '[href="/reviews"] span',
        "Блог": '[data-elem-id="176285426168494440"]',
    }

    for name, selector in menu_items.items():
        element = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, selector)
            )
        )
        assert element.is_displayed(), f"Не отображается: {name}"

    # Проверка переключателей языка
    for lang, selector in {
        "ru": '[href="/ru"]',
        "de": '[href="/"]',
    }.items():
        element = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, selector)
            )
        )
        assert element.is_displayed(), f"Нет переключателя {lang}"

    # Открытие выпадающего меню "О нас"
    about_us = driver.find_element(
        By.CSS_SELECTOR, '[href="#submenu:more2"] span'
    )
    ActionChains(driver).move_to_element(about_us).perform()

    # Проверка и переход в "Контакты"
    contacts = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '[href="/ru/contact-us"]')
        )
    )
    assert contacts.is_displayed()
    contacts.click()

    wait.until(EC.url_contains("https://itcareerhub.de/ru/contact-us"))

    # Поиск ссылки "Обратный звонок"
    callback = wait.until(
        EC.visibility_of_element_located(
            (
                By.CSS_SELECTOR,
                '[data-elem-id="1754046238620"] a[href="#popup:form-tr"]'
            )
        )
    )

    # Прокрутка к ссылке
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});",
        callback
    )

    # Клик через JavaScript
    driver.execute_script(
        "arguments[0].click();",
        callback
    )

    # Проверка текста во всплывающем окне
    popup_text = wait.until(
        EC.visibility_of_element_located(
            (
                By.CSS_SELECTOR,
                '[field="tn_text_175871291756015470"]'
            )
        )
    )

    assert (
            "Запишитесь на бесплатную карьерную консультацию"
            in popup_text.text
    ), "Текст консультации не отображается"
