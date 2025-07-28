import json
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Настройка десктопного браузера
@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 Chrome/113.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Убираем определения WebDriver
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            window.navigator.chrome = { runtime: {} };
            Object.defineProperty(navigator, 'languages', { get: () => ['ru-RU', 'ru'] });
            Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
        """
    })

    driver.get("https://www.kinopoisk.ru/")

    # Загрузка cookies
    try:
        with open("kinopoisk_cookies.json", "r", encoding="utf-8") as f:
            cookies = json.load(f)
        for cookie in cookies:
            if "domain" in cookie and "kinopoisk.ru" in cookie["domain"]:
                # Пропустить куки с неподходящим доменом (например, поддомены)
                if cookie.get("domain") != ".kinopoisk.ru":
                    continue
                try:
                    driver.add_cookie(cookie)
                except Exception as e:
                    print(f"Ошибка с кукой {cookie.get('name', 'unknown')}: {e}")
    except Exception as e:
        print(f"Ошибка загрузки cookies: {e}")

    driver.refresh()
    yield driver
    driver.quit()


# Отдельная фикстура для мобильной версии
@pytest.fixture
def mobile_driver():
    mobile_emulation = {
        "deviceMetrics": { "width": 375, "height": 667, "pixelRatio": 3.0 },
        "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) "
                     "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 "
                     "Mobile/15E148 Safari/604.1"
    }

    options = webdriver.ChromeOptions()
    options.add_experimental_option("mobileEmulation", mobile_emulation)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://www.kinopoisk.ru/")

    # Загрузка cookies
    try:
        with open("kinopoisk_cookies.json", "r", encoding="utf-8") as f:
            cookies = json.load(f)
        for cookie in cookies:
            if "domain" in cookie and "kinopoisk.ru" in cookie["domain"]:
                if cookie.get("domain") != ".kinopoisk.ru":
                    continue
                try:
                    driver.add_cookie(cookie)
                except Exception as e:
                    print(f"Ошибка с кукой {cookie.get('name', 'unknown')}: {e}")
    except Exception as e:
        print(f"Ошибка загрузки cookies: {e}")

    driver.refresh()
    yield driver
    driver.quit()
