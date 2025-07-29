@echo off
echo Запуск всех тестов (UI + API)...
python -m pytest --alluredir=allure-results

if %errorlevel% neq 0 (
    echo ❌ Некоторые тесты завершились с ошибкой.
) else (
    echo ✅ Все тесты успешно пройдены.
)

echo Открытие Allure-отчета...
allure serve allure-results
