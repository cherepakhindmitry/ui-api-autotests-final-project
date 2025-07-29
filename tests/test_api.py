import requests
import pytest
import allure

BASE_URL = "https://api.kinopoisk.dev/v1.4/movie"

HEADERS = {
    "X-API-KEY": "KYH5YAP-YWRMNDZ-M19C2YH-4ZV3BAE",
    "Content-Type": "application/json"
}


@pytest.mark.api
@allure.title("Поиск по названию на кириллице (Титаник)")
@allure.severity(allure.severity_level.CRITICAL)
def test_search_ru_title():
    with allure.step("Отправляем GET-запрос с query='Титаник'"):
        response = requests.get(
            f"{BASE_URL}/search",
            headers=HEADERS,
            params={"page": 1, "limit": 10, "query": "Титаник"}
        )
    with allure.step("Проверяем, что получен статус 200 и есть фильмы"):
        assert response.status_code == 200
        assert len(response.json().get("docs", [])) > 0


@pytest.mark.api
@allure.title("Поиск по названию на латинице (Titanic)")
@allure.severity(allure.severity_level.CRITICAL)
def test_search_en_title():
    with allure.step("Отправляем GET-запрос с query='Titanic'"):
        response = requests.get(
            f"{BASE_URL}/search",
            headers=HEADERS,
            params={"page": 1, "limit": 10, "query": "Titanic"}
        )
    with allure.step("Проверяем статус-код и наличие фильмов"):
        assert response.status_code == 200
        assert len(response.json().get("docs", [])) > 0


@pytest.mark.api
@allure.title("Поиск по названию с цифрами (Avatar 2)")
@allure.severity(allure.severity_level.NORMAL)
def test_search_with_numbers():
    with allure.step("GET-запрос с query='Avatar 2'"):
        response = requests.get(
            f"{BASE_URL}/search",
            headers=HEADERS,
            params={"page": 1, "limit": 10, "query": "Avatar 2"}
        )
    with allure.step("Ожидаем статус 200 и наличие результатов"):
        assert response.status_code == 200
        assert len(response.json().get("docs", [])) > 0


@pytest.mark.api
@allure.title("Поиск по жанру 'драма'")
@allure.severity(allure.severity_level.NORMAL)
def test_search_by_genre():
    with allure.step("GET-запрос с genres.name='драма'"):
        response = requests.get(
            BASE_URL,
            headers=HEADERS,
            params={"page": 1, "limit": 10, "genres.name": "драма"}
        )
    with allure.step("Проверяем, что жанр найден"):
        assert response.status_code == 200
        assert len(response.json().get("docs", [])) > 0


@pytest.mark.api
@allure.title("Поиск фильмов по году выпуска 2019")
@allure.severity(allure.severity_level.NORMAL)
def test_search_by_year():
    with allure.step("GET-запрос с параметром year=2019"):
        response = requests.get(
            BASE_URL,
            headers=HEADERS,
            params={"page": 1, "limit": 10, "year": 2019}
        )
    with allure.step("Ожидаем статус 200 и наличие фильмов"):
        assert response.status_code == 200
        assert len(response.json().get("docs", [])) > 0


@pytest.mark.api
@allure.title("Поиск по произвольному набору символов")
@allure.severity(allure.severity_level.MINOR)
def test_search_gibberish():
    with allure.step("GET-запрос с query='fgdhhywedvbt'"):
        response = requests.get(
            f"{BASE_URL}/search",
            headers=HEADERS,
            params={"page": 1, "limit": 10, "query": "fgdhhywedvbt"}
        )
    with allure.step("Ожидаем статус 200 и пустой список"):
        assert response.status_code == 200
        assert len(response.json().get("docs", [])) == 0


@pytest.mark.api
@allure.title("Поиск без токена авторизации")
@allure.severity(allure.severity_level.CRITICAL)
def test_search_without_token():
    with allure.step("GET-запрос без заголовка X-API-KEY"):
        response = requests.get(
            f"{BASE_URL}/search",
            headers={"Content-Type": "application/json"},
            params={"page": 1, "limit": 10, "query": "Титаник"}
        )
    with allure.step("Ожидаем статус 401 Unauthorized"):
        assert response.status_code == 401
