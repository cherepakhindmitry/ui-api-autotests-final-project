import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException


@allure.title("Поиск по названию фильма 'Интерстеллар'")
@allure.tag("UI", "search", "kinopoisk")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.ui
def test_search_interstellar(driver):
    with allure.step("Открываем главную страницу Кинопоиска"):
        driver.get("https://www.kinopoisk.ru/")

    with allure.step("Находим поле поиска и вводим 'Интерстеллар' с нажатием Enter"):
        try:
            search_input = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label*='Фильмы']"))
            )
            search_input.clear()
            search_input.send_keys("Интерстеллар")
            search_input.send_keys(Keys.RETURN)  # Нажимаем Enter
        except TimeoutException:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="search_input_not_found",
                attachment_type=allure.attachment_type.PNG
            )
            pytest.fail("❌ Поле поиска не найдено")

    with allure.step("Ожидаем появления результатов поиска и проверяем наличие 'Интерстеллар'"):
        try:
            result = WebDriverWait(driver, 25).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//a[contains(text(), 'Интерстеллар')]")
                )
            )
            assert result.is_displayed(), "❌ Фильм 'Интерстеллар' найден, но не отображается"
        except TimeoutException:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="interstellar_not_found",
                attachment_type=allure.attachment_type.PNG
            )
            pytest.fail("❌ Фильм 'Интерстеллар' не найден в результатах поиска")


@allure.title("Поиск несуществующего фильма")
@pytest.mark.ui
def test_search_nonexistent_film(driver):
    with allure.step("Открытие главной страницы"):
        driver.get("https://www.kinopoisk.ru/")

    with allure.step("Ввод запроса несуществующего фильма"):
        search_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[aria-label*='Фильмы']")
            )
        )
        search_input.clear()
        search_input.send_keys("ВасяПупкинВестерн")

    with allure.step("Ожидание появления выпадающих результатов"):
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class, 'header-search-form__suggest')]")
            )
        )

    with allure.step("Проверка отсутствия результатов"):
        no_results = driver.find_elements(By.XPATH, "//a[contains(text(), 'ВасяПупкинВестерн')]")
        assert len(no_results) == 0, "Найден неожиданный результат поиска!"


@allure.title("Подсказка в поле поиска")
@pytest.mark.ui
def test_search_field_placeholder(driver):
    with allure.step("Открытие главной страницы"):
        driver.get("https://www.kinopoisk.ru")

    with allure.step("Ожидание появления поля поиска"):
        search_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[aria-label*='Фильмы']")
            )
        )

    with allure.step("Фокус на поле поиска и ожидание появления подсказки"):
        search_input.click()
        time.sleep(5)  # ⏳ подождём 3 секунды, чтобы подсказки успели появиться

    with allure.step("Проверка наличия текста в плейсхолдере"):
        placeholder = search_input.get_attribute("placeholder")
        assert "Фильмы" in placeholder or "персоны" in placeholder, \
            f"Плейсхолдер не соответствует ожиданиям: '{placeholder}'"


@allure.title("Визуальная выделенность кнопки 'Войти' (hover-эффект)")
@pytest.mark.ui
def test_login_button_highlight(driver):
    with allure.step("Открытие главной страницы"):
        driver.get("https://www.kinopoisk.ru/")

    with allure.step("Ожидание появления кнопки 'Войти'"):
        button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//button[text()='Войти']"))
        )

    with allure.step("Проверка цвета кнопки до наведения мыши"):
        button_color_before = driver.find_element(By.XPATH, "//button[text()='Войти']").value_of_css_property("color")

    with allure.step("Наведение мыши на кнопку"):
        ActionChains(driver).move_to_element(button).perform()
        time.sleep(5)  # Пауза, чтобы визуально отобразился hover

    with allure.step("Проверка изменения цвета кнопки"):
        button_color_after = driver.find_element(By.XPATH, "//button[text()='Войти']").value_of_css_property("color")
        assert button_color_before != button_color_after


@allure.title("Адаптивность главной страницы Кинопоиска")
@pytest.mark.ui
def test_adaptive_layout(driver, mobile_driver):
    with allure.step("Открытие главной страницы в десктопной версии"):
        driver.get("https://www.kinopoisk.ru/")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//button[text()='Войти']"))
        )
        assert driver.find_element(By.XPATH, "//button[text()='Войти']").is_displayed(), \
            "Кнопка 'Войти' не отображается в десктопной версии"

    with allure.step("Открытие главной страницы в планшетной версии (эмуляция через resize)"):
        driver.set_window_size(1024, 768)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//button[text()='Войти']"))
        )
        assert driver.find_element(By.XPATH, "//button[text()='Войти']").is_displayed(), \
            "Кнопка 'Войти' не отображается в планшетной версии"

    with allure.step("Открытие главной страницы в мобильной версии (эмуляция iPhone)"):
        mobile_driver.get("https://www.kinopoisk.ru/")
        WebDriverWait(mobile_driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label*='меню'], button[aria-label*='Меню']"))
        )
        assert mobile_driver.find_element(By.CSS_SELECTOR,
                                          "button[aria-label*='меню'],"
                                          " button[aria-label*='Меню']"
                                          ).is_displayed(), \
            "Мобильное меню не отображается в мобильной версии"
