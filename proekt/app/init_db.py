"""
Модуль для инициализации базы данных тестовыми данными
"""
import sys
import os

# Добавляем корневую директорию в путь Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.db import SessionLocal, create_tables
from app.db import crud, models


def init_database():
    """
    Инициализирует базу данных тестовыми данными
    """
    print("🚀 Начало инициализации базы данных...")
    
    # Создаем сессию
    db = SessionLocal()
    
    try:
        # Создаем таблицы
        print("📋 Создание таблиц...")
        create_tables()
        
        # Создаем категории
        print("🏷️  Добавление категорий...")
        
        categories_data = [
            {"title": "Научная фантастика"},
            {"title": "Фэнтези"},
            {"title": "Детективы"},
            {"title": "Программирование"}
        ]
        
        categories = []
        for cat_data in categories_data:
            category = crud.create_category(db, title=cat_data["title"])
            categories.append(category)
            print(f"  ✅ Добавлена категория: {category.title} (ID: {category.id})")
        
        # Создаем книги для каждой категории
        print("📚 Добавление книг...")
        
        books_data = [
            # Научная фантастика
            {
                "title": "Дюна",
                "description": "Эпическая сага о пустынной планете Арракис",
                "price": 899.99,
                "category_id": categories[0].id
            },
            {
                "title": "451° по Фаренгейту",
                "description": "Антиутопия о мире, где книги запрещены",
                "price": 599.50,
                "category_id": categories[0].id
            },
            {
                "title": "Нейромант",
                "description": "Роман, положивший начало жанру киберпанк",
                "price": 750.00,
                "category_id": categories[0].id
            },
            
            # Фэнтези
            {
                "title": "Властелин колец",
                "description": "Эпическая трилогия о Средиземье",
                "price": 1299.99,
                "category_id": categories[1].id
            },
            {
                "title": "Гарри Поттер и философский камень",
                "description": "Первая книга о юном волшебнике",
                "price": 699.99,
                "category_id": categories[1].id
            },
            
            # Детективы
            {
                "title": "Убийство в Восточном экспрессе",
                "description": "Знаменитый детектив Агаты Кристи",
                "price": 450.00,
                "category_id": categories[2].id
            },
            {
                "title": "Шерлок Холмс: Сборник рассказов",
                "description": "Приключения великого сыщика",
                "price": 550.00,
                "category_id": categories[2].id
            },
            
            # Программирование
            {
                "title": "Чистый код",
                "description": "Создание, анализ и рефакторинг",
                "price": 1200.00,
                "category_id": categories[3].id
            },
            {
                "title": "Совершенный код",
                "description": "Полное руководство по созданию ПО",
                "price": 1500.00,
                "category_id": categories[3].id
            },
            {
                "title": "Python. К вершинам мастерства",
                "description": "Продвинутое руководство по Python",
                "price": 999.99,
                "category_id": categories[3].id
            },
            {
                "title": "Грокаем алгоритмы",
                "description": "Иллюстрированное руководство",
                "price": 850.00,
                "category_id": categories[3].id
            }
        ]
        
        for book_data in books_data:
            book = crud.create_book(
                db=db,
                title=book_data["title"],
                description=book_data["description"],
                price=book_data["price"],
                category_id=book_data["category_id"],
                url="https://example.com/book-details"  # Пример URL
            )
            print(f"  ✅ Добавлена книга: {book.title} - {book.price} руб.")
        
        # Выводим статистику
        print("\n📊 Статистика базы данных:")
        categories_count = len(crud.get_all_categories(db))
        books_count = len(crud.get_all_books(db))
        
        print(f"   Категорий: {categories_count}")
        print(f"   Книг: {books_count}")
        
        # Выводим книги по категориям
        print("\n📖 Книги по категориям:")
        for category in categories:
            books_in_category = crud.get_books_by_category(db, category.id)
            print(f"   {category.title}: {len(books_in_category)} книг")
        
        print("\n🎉 Инициализация базы данных завершена успешно!")
        
    except Exception as e:
        print(f"❌ Ошибка при инициализации: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_database()
