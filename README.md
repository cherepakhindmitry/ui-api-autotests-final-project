# UI и API тестирование сайта Кинопоиск

## 📋 Описание проекта

Курсовой проект по автоматизации UI- и API-тестирования с использованием **Selenium**, **pytest**, **requests** и **Allure**.

Проект направлен на проверку базовой функциональности сайта [https://www.kinopoisk.ru](https://www.kinopoisk.ru) и его неофициального API: поиск фильмов, отображение подсказок, корректность интерфейса, адаптивность, получение данных о фильмах и др.

## ⚙️ Стек технологий

- Python 3.13
- Selenium
- Requests
- Pytest
- Allure
- WebDriver Manager

## 📁 Структура проекта

```
final-project/
├── tests/
│   ├── test_ui.py             # Все UI-тесты
│   └── test_api.py            # Все API-тесты
├── conftest.py                # Фикстуры и инициализация драйвера
├── pytest.ini                 # Настройки Pytest и теги
├── requirements.txt           # Зависимости проекта
├── run_tests.bat              # Сценарий запуска UI + API тестов
├── .gitignore
└── README.md                  # Этот файл
```

## ✅ Реализованные тесты

### UI-тесты

1. **Поиск по названию фильма 'Интерстеллар'**
2. **Поиск несуществующего фильма**
3. **Подсказка в поле поиска**
4. **Визуальная выделенность кнопки 'Войти' (hover-эффект)**
5. **Адаптивность главной страницы Кинопоиска**

### API-тесты

1. **Получение информации о фильме по ID**
2. **Поиск фильма по ключевому слову**
3. **Запрос несуществующего фильма**
4. **Проверка списка топ-100 популярных фильмов**
5. **Получение фактов о фильме**
6. **Поиск фильма на кириллице ("Титаник")**

## 📦 Установка

```bash
git clone https://github.com/cherepakhindmitry/ui-api-autotests-final-project.git
cd ui-api-autotests-final-project
pip install -r requirements.txt
```

## 🚀 Запуск тестов

### Все тесты (UI + API)
```bash
python -m pytest --alluredir=allure-results
allure serve allure-results
```

### Только UI:
```bash
python -m pytest -m ui --alluredir=allure-results
```

### Только API:
```bash
python -m pytest -m api --alluredir=allure-results
```

### Через `.bat`-файл:
```cmd
run_tests.bat

Файл run_tests.bat предназначен только для Windows.
Пользователям macOS и Linux необходимо запускать тесты через команду:
python -m pytest --alluredir=allure-results
allure serve allure-results
```

## 🔐 Примечания

- Для UI-тестов используется обход капчи через сохранение cookies.
- Эмуляция мобильного устройства (iPhone X) осуществляется через DevTools.
- API-ключ подключён из переменной окружения / config-файла.

## 📎 Ссылка на проект по ручному тестированию
[Финальная работа (ручное тестирование)](https://cherepakhindmitry.yonote.ru/share/d970c7f8-8a29-48b1-bb9c-1ef0b4209184)
