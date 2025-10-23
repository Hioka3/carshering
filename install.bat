@echo off
echo ========================================
echo     УСТАНОВКА КАРШЕРИНГ ПРИЛОЖЕНИЯ
echo ========================================
echo.

echo Создание виртуального окружения...
python -m venv .venv

echo.
echo Активация виртуального окружения...
call .venv\Scripts\activate.bat

echo.
echo Обновление pip...
python -m pip install --upgrade pip

echo.
echo Установка зависимостей из requirements.txt...
pip install -r requirements.txt

echo.
echo ========================================
echo     УСТАНОВКА ЗАВЕРШЕНА!
echo ========================================
echo.
echo Для запуска приложения:
echo 1. Инициализируйте базу данных: python backend/init_db.py
echo 2. Запустите сервер: python backend/server.py
echo 3. Запустите админ-панель: python backend/admin_panel.py
echo 4. Откройте web/index.html в браузере
echo.
pause