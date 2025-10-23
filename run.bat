@echo off
echo ========================================
echo      ЗАПУСК КАРШЕРИНГ ПРИЛОЖЕНИЯ
echo ========================================
echo.

echo Активация виртуального окружения...
call .venv\Scripts\activate.bat

echo.
echo Инициализация базы данных...
python backend/init_db.py

echo.
echo ========================================
echo Выберите компонент для запуска:
echo 1. Запустить веб-сервер (Flask)
echo 2. Запустить админ-панель (Tkinter)
echo 3. Открыть веб-интерфейс в браузере
echo 4. Запустить все компоненты
echo ========================================
set /p choice="Введите номер (1-4): "

if "%choice%"=="1" (
    echo Запуск веб-сервера...
    python backend/server.py
)
if "%choice%"=="2" (
    echo Запуск админ-панели...
    python backend/admin_panel.py
)
if "%choice%"=="3" (
    echo Открытие веб-интерфейса...
    start web/index.html
)
if "%choice%"=="4" (
    echo Запуск всех компонентов...
    start "Веб-сервер" cmd /k "call .venv\Scripts\activate.bat && python backend/server.py"
    start "Админ-панель" cmd /k "call .venv\Scripts\activate.bat && python backend/admin_panel.py"
    timeout /t 2 /nobreak >nul
    start web/index.html
    echo Все компоненты запущены!
)

echo.
pause