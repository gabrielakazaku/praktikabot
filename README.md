# PostgreSQL SQLAlchemy Project

Проект для работы с PostgreSQL через SQLAlchemy с реализацией CRUD операций.

## Структура проекта
- `app/db/db.py` - подключение к базе данных
- `app/db/models.py` - модели SQLAlchemy
- `app/db/crud.py` - CRUD операции
- `app/init_db.py` - инициализация базы данных
- `app/main.py` - основное приложение
- `.env` - переменные окружения
- `requirements.txt` - зависимости Python

## Установка
1. Установите PostgreSQL и создайте БД `octagon_db`
2. Создайте виртуальное окружение: `python -m venv venv`
3. Установите зависимости: `pip install -r requirements.txt`
4. Запустите инициализацию: `python app/init_db.py`
5. Запустите приложение: `python app/main.py`

## Использование
Приложение предоставляет интерактивное меню для:
- Просмотра категорий и книг
- Поиска книг
- Просмотра статистики
