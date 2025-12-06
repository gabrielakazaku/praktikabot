"""
Основной модуль приложения для работы с базой данных
"""
import sys
import os
from tabulate import tabulate

# Добавляем корневую директорию в путь Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.db import SessionLocal
from app.db import crud


def display_categories():
    """Отображает все категории"""
    db = SessionLocal()
    try:
        categories = crud.get_all_categories(db)
        
        print("=" * 60)
        print("📚 КАТЕГОРИИ КНИГ")
        print("=" * 60)
        
        if not categories:
            print("Категории не найдены")
            return
        
        # Формируем данные для таблицы
        table_data = []
        for category in categories:
            books_count = len(crud.get_books_by_category(db, category.id))
            table_data.append([
                category.id,
                category.title,
                books_count
            ])
        
        # Выводим таблицу
        headers = ["ID", "Название категории", "Кол-во книг"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        print()
        
    finally:
        db.close()


def display_books():
    """Отображает все книги с информацией о категориях"""
    db = SessionLocal()
    try:
        books_with_categories = crud.get_books_with_categories(db)
        
        print("=" * 60)
        print("📖 ВСЕ КНИГИ")
        print("=" * 60)
        
        if not books_with_categories:
            print("Книги не найдены")
            return
        
        # Формируем данные для таблицы
        table_data = []
        for book in books_with_categories:
            table_data.append([
                book["book_id"],
                book["book_title"],
                f'{book["book_price"]:.2f} руб.',
                book["category_title"],
                (book["book_description"][:50] + "...") if book["book_description"] and len(book["book_description"]) > 50 else book["book_description"]
            ])
        
        # Выводим таблицу
        headers = ["ID", "Название книги", "Цена", "Категория", "Описание (первые 50 символов)"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        print()
        
    finally:
        db.close()


def display_books_by_category(category_id: int):
    """Отображает книги определенной категории"""
    db = SessionLocal()
    try:
        category = crud.get_category(db, category_id)
        if not category:
            print(f"❌ Категория с ID {category_id} не найдена")
            return
        
        books = crud.get_books_by_category(db, category_id)
        
        print("=" * 60)
        print(f"📚 КНИГИ В КАТЕГОРИИ: {category.title}")
        print("=" * 60)
        
        if not books:
            print("Книги не найдены")
            return
        
        # Формируем данные для таблицы
        table_data = []
        for book in books:
            table_data.append([
                book.id,
                book.title,
                f'{book.price:.2f} руб.',
                (book.description[:60] + "...") if book.description and len(book.description) > 60 else book.description
            ])
        
        # Выводим таблицу
        headers = ["ID", "Название", "Цена", "Описание"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        print()
        
    finally:
        db.close()


def display_statistics():
    """Отображает статистику базы данных"""
    db = SessionLocal()
    try:
        categories = crud.get_all_categories(db)
        all_books = crud.get_all_books(db)
        
        print("=" * 60)
        print("📊 СТАТИСТИКА БАЗЫ ДАННЫХ")
        print("=" * 60)
        
        print(f"Всего категорий: {len(categories)}")
        print(f"Всего книг: {len(all_books)}")
        print()
        
        print("📈 Распределение книг по категориям:")
        print("-" * 40)
        
        stats_data = []
        for category in categories:
            books_in_category = crud.get_books_by_category(db, category.id)
            stats_data.append([
                category.title,
                len(books_in_category),
                f"{(len(books_in_category) / len(all_books) * 100):.1f}%"
            ])
        
        headers = ["Категория", "Кол-во книг", "Процент"]
        print(tabulate(stats_data, headers=headers, tablefmt="simple"))
        print()
        
        # Самая дорогая и дешевая книга
        if all_books:
            most_expensive = max(all_books, key=lambda x: x.price)
            cheapest = min(all_books, key=lambda x: x.price)
            
            print("💰 Интересные факты:")
            print(f"  Самая дорогая книга: '{most_expensive.title}' - {most_expensive.price:.2f} руб.")
            print(f"  Самая дешевая книга: '{cheapest.title}' - {cheapest.price:.2f} руб.")
            print(f"  Средняя цена: {sum(b.price for b in all_books) / len(all_books):.2f} руб.")
        
    finally:
        db.close()


def search_books_interactive():
    """Интерактивный поиск книг"""
    db = SessionLocal()
    try:
        print("🔍 ПОИСК КНИГ")
        print("-" * 40)
        
        search_term = input("Введите название или часть описания для поиска: ").strip()
        
        if not search_term:
            print("❌ Поисковый запрос не может быть пустым")
            return
        
        books = crud.search_books(db, search_term)
        
        print(f"\n📖 Найдено книг: {len(books)}")
        
        if books:
            table_data = []
            for book in books:
                category = crud.get_category(db, book.category_id)
                table_data.append([
                    book.id,
                    book.title,
                    f'{book.price:.2f} руб.',
                    category.title if category else "Неизвестно",
                    (book.description[:50] + "...") if book.description and len(book.description) > 50 else book.description
                ])
            
            headers = ["ID", "Название", "Цена", "Категория", "Описание"]
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
        else:
            print("Книги по вашему запросу не найдены")
        
        print()
        
    finally:
        db.close()


def main_menu():
    """Главное меню приложения"""
    while True:
        print("\n" + "=" * 60)
        print("📚 СИСТЕМА УПРАВЛЕНИЯ БИБЛИОТЕКОЙ")
        print("=" * 60)
        print("1. Показать все категории")
        print("2. Показать все книги")
        print("3. Показать книги по категории")
        print("4. Показать статистику")
        print("5. Поиск книг")
        print("6. Выйти")
        print("-" * 60)
        
        choice = input("Выберите действие (1-6): ").strip()
        
        if choice == "1":
            display_categories()
        elif choice == "2":
            display_books()
        elif choice == "3":
            try:
                category_id = int(input("Введите ID категории: "))
                display_books_by_category(category_id)
            except ValueError:
                print("❌ Ошибка: введите число")
        elif choice == "4":
            display_statistics()
        elif choice == "5":
            search_books_interactive()
        elif choice == "6":
            print("👋 До свидания!")
            break
        else:
            print("❌ Неверный выбор. Попробуйте снова.")
        
        input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    # Устанавливаем tabulate, если его нет
    try:
        import tabulate
    except ImportError:
        print("Установка необходимой библиотеки tabulate...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "tabulate"])
        import tabulate
    
    print("🚀 Запуск системы управления библиотекой")
    print("📊 Подключение к базе данных...")
    
    # Проверяем подключение
    db = SessionLocal()
    try:
        # Простая проверка подключения
        categories_count = len(crud.get_all_categories(db))
        books_count = len(crud.get_all_books(db))
        print(f"✅ Подключение установлено")
        print(f"📚 В базе: {categories_count} категорий, {books_count} книг")
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        print("⚠️  Возможно, база данных не инициализирована.")
        print("   Запустите сначала: python app/init_db.py")
        exit(1)
    finally:
        db.close()
    
    # Запускаем главное меню
    main_menu()
EOFcat > app/main.py << 'EOF'
"""
Основной модуль приложения для работы с базой данных
"""
import sys
import os
from tabulate import tabulate

# Добавляем корневую директорию в путь Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.db import SessionLocal
from app.db import crud


def display_categories():
    """Отображает все категории"""
    db = SessionLocal()
    try:
        categories = crud.get_all_categories(db)
        
        print("=" * 60)
        print("📚 КАТЕГОРИИ КНИГ")
        print("=" * 60)
        
        if not categories:
            print("Категории не найдены")
            return
        
        # Формируем данные для таблицы
        table_data = []
        for category in categories:
            books_count = len(crud.get_books_by_category(db, category.id))
            table_data.append([
                category.id,
                category.title,
                books_count
            ])
        
        # Выводим таблицу
        headers = ["ID", "Название категории", "Кол-во книг"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        print()
        
    finally:
        db.close()


def display_books():
    """Отображает все книги с информацией о категориях"""
    db = SessionLocal()
    try:
        books_with_categories = crud.get_books_with_categories(db)
        
        print("=" * 60)
        print("📖 ВСЕ КНИГИ")
        print("=" * 60)
        
        if not books_with_categories:
            print("Книги не найдены")
            return
        
        # Формируем данные для таблицы
        table_data = []
        for book in books_with_categories:
            table_data.append([
                book["book_id"],
                book["book_title"],
                f'{book["book_price"]:.2f} руб.',
                book["category_title"],
                (book["book_description"][:50] + "...") if book["book_description"] and len(book["book_description"]) > 50 else book["book_description"]
            ])
        
        # Выводим таблицу
        headers = ["ID", "Название книги", "Цена", "Категория", "Описание (первые 50 символов)"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        print()
        
    finally:
        db.close()


def display_books_by_category(category_id: int):
    """Отображает книги определенной категории"""
    db = SessionLocal()
    try:
        category = crud.get_category(db, category_id)
        if not category:
            print(f"❌ Категория с ID {category_id} не найдена")
            return
        
        books = crud.get_books_by_category(db, category_id)
        
        print("=" * 60)
        print(f"📚 КНИГИ В КАТЕГОРИИ: {category.title}")
        print("=" * 60)
        
        if not books:
            print("Книги не найдены")
            return
        
        # Формируем данные для таблицы
        table_data = []
        for book in books:
            table_data.append([
                book.id,
                book.title,
                f'{book.price:.2f} руб.',
                (book.description[:60] + "...") if book.description and len(book.description) > 60 else book.description
            ])
        
        # Выводим таблицу
        headers = ["ID", "Название", "Цена", "Описание"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        print()
        
    finally:
        db.close()


def display_statistics():
    """Отображает статистику базы данных"""
    db = SessionLocal()
    try:
        categories = crud.get_all_categories(db)
        all_books = crud.get_all_books(db)
        
        print("=" * 60)
        print("📊 СТАТИСТИКА БАЗЫ ДАННЫХ")
        print("=" * 60)
        
        print(f"Всего категорий: {len(categories)}")
        print(f"Всего книг: {len(all_books)}")
        print()
        
        print("📈 Распределение книг по категориям:")
        print("-" * 40)
        
        stats_data = []
        for category in categories:
            books_in_category = crud.get_books_by_category(db, category.id)
            stats_data.append([
                category.title,
                len(books_in_category),
                f"{(len(books_in_category) / len(all_books) * 100):.1f}%"
            ])
        
        headers = ["Категория", "Кол-во книг", "Процент"]
        print(tabulate(stats_data, headers=headers, tablefmt="simple"))
        print()
        
        # Самая дорогая и дешевая книга
        if all_books:
            most_expensive = max(all_books, key=lambda x: x.price)
            cheapest = min(all_books, key=lambda x: x.price)
            
            print("💰 Интересные факты:")
            print(f"  Самая дорогая книга: '{most_expensive.title}' - {most_expensive.price:.2f} руб.")
            print(f"  Самая дешевая книга: '{cheapest.title}' - {cheapest.price:.2f} руб.")
            print(f"  Средняя цена: {sum(b.price for b in all_books) / len(all_books):.2f} руб.")
        
    finally:
        db.close()


def search_books_interactive():
    """Интерактивный поиск книг"""
    db = SessionLocal()
    try:
        print("🔍 ПОИСК КНИГ")
        print("-" * 40)
        
        search_term = input("Введите название или часть описания для поиска: ").strip()
        
        if not search_term:
            print("❌ Поисковый запрос не может быть пустым")
            return
        
        books = crud.search_books(db, search_term)
        
        print(f"\n📖 Найдено книг: {len(books)}")
        
        if books:
            table_data = []
            for book in books:
                category = crud.get_category(db, book.category_id)
                table_data.append([
                    book.id,
                    book.title,
                    f'{book.price:.2f} руб.',
                    category.title if category else "Неизвестно",
                    (book.description[:50] + "...") if book.description and len(book.description) > 50 else book.description
                ])
            
            headers = ["ID", "Название", "Цена", "Категория", "Описание"]
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
        else:
            print("Книги по вашему запросу не найдены")
        
        print()
        
    finally:
        db.close()


def main_menu():
    """Главное меню приложения"""
    while True:
        print("\n" + "=" * 60)
        print("📚 СИСТЕМА УПРАВЛЕНИЯ БИБЛИОТЕКОЙ")
        print("=" * 60)
        print("1. Показать все категории")
        print("2. Показать все книги")
        print("3. Показать книги по категории")
        print("4. Показать статистику")
        print("5. Поиск книг")
        print("6. Выйти")
        print("-" * 60)
        
        choice = input("Выберите действие (1-6): ").strip()
        
        if choice == "1":
            display_categories()
        elif choice == "2":
            display_books()
        elif choice == "3":
            try:
                category_id = int(input("Введите ID категории: "))
                display_books_by_category(category_id)
            except ValueError:
                print("❌ Ошибка: введите число")
        elif choice == "4":
            display_statistics()
        elif choice == "5":
            search_books_interactive()
        elif choice == "6":
            print("👋 До свидания!")
            break
        else:
            print("❌ Неверный выбор. Попробуйте снова.")
        
        input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    # Устанавливаем tabulate, если его нет
    try:
        import tabulate
    except ImportError:
        print("Установка необходимой библиотеки tabulate...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "tabulate"])
        import tabulate
    
    print("🚀 Запуск системы управления библиотекой")
    print("📊 Подключение к базе данных...")
    
    # Проверяем подключение
    dcat > app/main.py << 'EOF'
"""
Основной модуль приложения для работы с базой данных
"""
import sys
import os
from tabulate import tabulate

# Добавляем корневую директорию в путь Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.db import SessionLocal
from app.db import crud


def display_categories():
    """Отображает все категории"""
    db = SessionLocal()
    try:
        categories = crud.get_all_categories(db)
        
        print("=" * 60)
        print("📚 КАТЕГОРИИ КНИГ")
        print("=" * 60)
        
        if not categories:
            print("Категории не найдены")
            return
        
        # Формируем данные для таблицы
        table_data = []
        for category in categories:
            books_count = len(crud.get_books_by_category(db, category.id))
            table_data.append([
                category.id,
                category.title,
                books_count
            ])
        
        # Выводим таблицу
        headers = ["ID", "Название категории", "Кол-во книг"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        print()
        
    finally:
        db.close()


def display_books():
    """Отображает все книги с информацией о категориях"""
    db = SessionLocal()
    try:
        books_with_categories = crud.get_books_with_categories(db)
        
        print("=" * 60)
        print("📖 ВСЕ КНИГИ")
        print("=" * 60)
        
        if not books_with_categories:
            print("Книги не найдены")
            return
        
        # Формируем данные для таблицы
        table_data = []
        for book in books_with_categories:
            table_data.append([
                book["book_id"],
                book["book_title"],
                f'{book["book_price"]:.2f} руб.',
                book["category_title"],
                (book["book_description"][:50] + "...") if book["book_description"] and len(book["book_description"]) > 50 else book["book_description"]
            ])
        
        # Выводим таблицу
        headers = ["ID", "Название книги", "Цена", "Категория", "Описание (первые 50 символов)"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        print()
        
    finally:
        db.close()


def display_books_by_category(category_id: int):
    """Отображает книги определенной категории"""
    db = SessionLocal()
    try:
        category = crud.get_category(db, category_id)
        if not category:
            print(f"❌ Категория с ID {category_id} не найдена")
            return
        
        books = crud.get_books_by_category(db, category_id)
        
        print("=" * 60)
        print(f"📚 КНИГИ В КАТЕГОРИИ: {category.title}")
        print("=" * 60)
        
        if not books:
            print("Книги не найдены")
            return
        
        # Формируем данные для таблицы
        table_data = []
        for book in books:
            table_data.append([
                book.id,
                book.title,
                f'{book.price:.2f} руб.',
                (book.description[:60] + "...") if book.description and len(book.description) > 60 else book.description
            ])
        
        # Выводим таблицу
        headers = ["ID", "Название", "Цена", "Описание"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        print()
        
    finally:
        db.close()


def display_statistics():
    """Отображает статистику базы данных"""
    db = SessionLocal()
    try:
        categories = crud.get_all_categories(db)
        all_books = crud.get_all_books(db)
        
        print("=" * 60)
        print("📊 СТАТИСТИКА БАЗЫ ДАННЫХ")
        print("=" * 60)
        
        print(f"Всего категорий: {len(categories)}")
        print(f"Всего книг: {len(all_books)}")
        print()
        
        print("📈 Распределение книг по категориям:")
        print("-" * 40)
        
        stats_data = []
        for category in categories:
            books_in_category = crud.get_books_by_category(db, category.id)
            stats_data.append([
                category.title,
                len(books_in_category),
                f"{(len(books_in_category) / len(all_books) * 100):.1f}%"
            ])
        
        headers = ["Категория", "Кол-во книг", "Процент"]
        print(tabulate(stats_data, headers=headers, tablefmt="simple"))
        print()
        
        # Самая дорогая и дешевая книга
        if all_books:
            most_expensive = max(all_books, key=lambda x: x.price)
            cheapest = min(all_books, key=lambda x: x.price)
            
            print("💰 Интересные факты:")
            print(f"  Самая дорогая книга: '{most_expensive.title}' - {most_expensive.price:.2f} руб.")
            print(f"  Самая дешевая книга: '{cheapest.title}' - {cheapest.price:.2f} руб.")
            print(f"  Средняя цена: {sum(b.price for b in all_books) / len(all_books):.2f} руб.")
        
    finally:
        db.close()


def search_books_interactive():
    """Интерактивный поиск книг"""
    db = SessionLocal()
    try:
        print("🔍 ПОИСК КНИГ")
        print("-" * 40)
        
        search_term = input("Введите название или часть описания для поиска: ").strip()
        
        if not search_term:
            print("❌ Поисковый запрос не может быть пустым")
            return
        
        books = crud.search_books(db, search_term)
        
        print(f"\n📖 Найдено книг: {len(books)}")
        
        if books:
            table_data = []
            for book in books:
                category = crud.get_category(db, book.category_id)
                table_data.append([
                    book.id,
                    book.title,
                    f'{book.price:.2f} руб.',
                    category.title if category else "Неизвестно",
                    (book.description[:50] + "...") if book.description and len(book.description) > 50 else book.description
                ])
            
            headers = ["ID", "Название", "Цена", "Категория", "Описание"]
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
        else:
            print("Книги по вашему запросу не найдены")
        
        print()
        
    finally:
        db.close()


def main_menu():
    """Главное меню приложения"""
    while True:
        print("\n" + "=" * 60)
        print("📚 СИСТЕМА УПРАВЛЕНИЯ БИБЛИОТЕКОЙ")
        print("=" * 60)
        print("1. Показать все категории")
        print("2. Показать все книги")
        print("3. Показать книги по категории")
        print("4. Показать статистику")
        print("5. Поиск книг")
        print("6. Выйти")
        print("-" * 60)
        
        choice = input("Выберите действие (1-6): ").strip()
        
        if choice == "1":
            display_categories()
        elif choice == "2":
            display_books()
        elif choice == "3":
            try:
                category_id = int(input("Введите ID категории: "))
                display_books_by_category(category_id)
            except ValueError:
                print("❌ Ошибка: введите число")
        elif choice == "4":
            display_statistics()
        elif choice == "5":
            search_books_interactive()
        elif choice == "6":
            print("👋 До свидания!")
            break
        else:
            print("❌ Неверный выбор. Попробуйте снова.")
        
        input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    # Устанавливаем tabulate, если его нет
    try:
        import tabulate
    except ImportError:
        print("Установка необходимой библиотеки tabulate...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "tabulate"])
        import tabulate
    
    print("🚀 Запуск системы управления библиотекой")
    print("📊 Подключение к базе данных...")
    
    # Проверяем подключение
    db = SessionLocal()
    try:
        # Простая проверка подключения
        categories_count = len(crud.get_all_categories(db))
        books_count = len(crud.get_all_books(db))
        print(f"✅ Подключение установлено")
        print(f"📚 В базе: {categories_count} категорий, {books_count} книг")
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        print("⚠️  Возможно, база данных не инициализирована.")
        print("   Запустите сначала: python app/init_db.py")
        exit(1)
    finally:
        db.close()
    
    cat > app/main.py << 'EOF'
"""
Основной модуль приложения для работы с базой данных
"""
import sys
import os
from tabulate import tabulate

# Добавляем корневую директорию в путь Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.db import SessionLocal
from app.db import crud


def display_categories():
    """Отображает все категории"""
    db = SessionLocal()
    try:
        categories = crud.get_all_categories(db)
        
        print("=" * 60)
        print("📚 КАТЕГОРИИ КНИГ")
        print("=" * 60)
        
        if not categories:
            print("Категории не найдены")
            return
        
        # Формируем данные для таблицы
        table_data = []
        for category in categories:
            books_count = len(crud.get_books_by_category(db, category.id))
            table_data.append([
                category.id,
                category.title,
                books_count
            ])
        
        # Выводим таблицу
        headers = ["ID", "Название категории", "Кол-во книг"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        print()
        
    finally:
        db.close()


def display_books():
    """Отображает все книги с информацией о категориях"""
    db = SessionLocal()
    try:
        books_with_categories = crud.get_books_with_categories(db)
        
        print("=" * 60)
        print("📖 ВСЕ КНИГИ")
        print("=" * 60)
        
        if not books_with_categories:
            print("Книги не найдены")
            return
        
        # Формируем данные для таблицы
        table_data = []
        for book in books_with_categories:
            table_data.append([
                book["book_id"],
                book["book_title"],
                f'{book["book_price"]:.2f} руб.',
                book["category_title"],
                (book["book_description"][:50] + "...") if book["book_description"] and len(book["book_description"]) > 50 else book["book_description"]
            ])
        
        # Выводим таблицу
        headers = ["ID", "Название книги", "Цена", "Категория", "Описание (первые 50 символов)"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        print()
        
    finally:
        db.close()


def display_books_by_category(category_id: int):
    """Отображает книги определенной категории"""
    db = SessionLocal()
    try:
        category = crud.get_category(db, category_id)
        if not category:
            print(f"❌ Категория с ID {category_id} не найдена")
            return
        
        books = crud.get_books_by_category(db, category_id)
        
        print("=" * 60)
        print(f"📚 КНИГИ В КАТЕГОРИИ: {category.title}")
        print("=" * 60)
        
        if not books:
            print("Книги не найдены")
            return
        
        # Формируем данные для таблицы
        table_data = []
        for book in books:
            table_data.append([
                book.id,
                book.title,
                f'{book.price:.2f} руб.',
                (book.description[:60] + "...") if book.description and len(book.description) > 60 else book.description
            ])
        
        # Выводим таблицу
        headers = ["ID", "Название", "Цена", "Описание"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        print()
        
    finally:
        db.close()


def display_statistics():
    """Отображает статистику базы данных"""
    db = SessionLocal()
    try:
        categories = crud.get_all_categories(db)
        all_books = crud.get_all_books(db)
        
        print("=" * 60)
        print("📊 СТАТИСТИКА БАЗЫ ДАННЫХ")
        print("=" * 60)
        
        print(f"Всего категорий: {len(categories)}")
        print(f"Всего книг: {len(all_books)}")
        print()
        
        print("📈 Распределение книг по категориям:")
        print("-" * 40)
        
        stats_data = []
        for category in categories:
            books_in_category = crud.get_books_by_category(db, category.id)
            stats_data.append([
                category.title,
                len(books_in_category),
                f"{(len(books_in_category) / len(all_books) * 100):.1f}%"
            ])
        
        headers = ["Категория", "Кол-во книг", "Процент"]
        print(tabulate(stats_data, headers=headers, tablefmt="simple"))
        print()
        
        # Самая дорогая и дешевая книга
        if all_books:
            most_expensive = max(all_books, key=lambda x: x.price)
            cheapest = min(all_books, key=lambda x: x.price)
            
            print("💰 Интересные факты:")
            print(f"  Самая дорогая книга: '{most_expensive.title}' - {most_expensive.price:.2f} руб.")
            print(f"  Самая дешевая книга: '{cheapest.title}' - {cheapest.price:.2f} руб.")
            print(f"  Средняя цена: {sum(b.price for b in all_books) / len(all_books):.2f} руб.")
        
    finally:
        db.close()


def search_books_interactive():
    """Интерактивный поиск книг"""
    db = SessionLocal()
    try:
        print("🔍 ПОИСК КНИГ")
        print("-" * 40)
        
        search_term = input("Введите название или часть описания для поиска: ").strip()
        
        if not search_term:
            print("❌ Поисковый запрос не может быть пустым")
            return
        
        books = crud.search_books(db, search_term)
        
        print(f"\n📖 Найдено книг: {len(books)}")
        
        if books:
            table_data = []
            for book in books:
                category = crud.get_category(db, book.category_id)
                table_data.append([
                    book.id,
                    book.title,
                    f'{book.price:.2f} руб.',
                    category.title if category else "Неизвестно",
                    (book.description[:50] + "...") if book.description and len(book.description) > 50 else book.description
                ])
            
            headers = ["ID", "Название", "Цена", "Категория", "Описание"]
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
        else:
            print("Книги по вашему запросу не найдены")
        
        print()
        
    finally:
        db.close()


def main_menu():
    """Главное меню приложения"""
    while True:
        print("\n" + "=" * 60)
        print("📚 СИСТЕМА УПРАВЛЕНИЯ БИБЛИОТЕКОЙ")
        print("=" * 60)
        print("1. Показать все категории")
        print("2. Показать все книги")
        print("3. Показать книги по категории")
        print("4. Показать статистику")
        print("5. Поиск книг")
        print("6. Выйти")
        print("-" * 60)
        
        choice = input("Выберите действие (1-6): ").strip()
        
        if choice == "1":
            display_categories()
        elif choice == "2":
            display_books()
        elif choice == "3":
            try:
                category_id = int(input("Введите ID категории: "))
                display_books_by_category(category_id)
            except ValueError:
                print("❌ Ошибка: введите число")
        elif choice == "4":
            display_statistics()
        elif choice == "5":
            search_books_interactive()
        elif choice == "6":
            print("👋 До свидания!")
            break
        else:
            print("❌ Неверный выбор. Попробуйте снова.")
        
        input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    # Устанавливаем tabulate, если его нет
    try:
        import tabulate
    except ImportError:
        print("Установка необходимой библиотеки tabulate...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "tabulate"])
        import tabulate
    
    print("🚀 Запуск системы управления библиотекой")
    print("📊 Подключение к базе данных...")
    
    # Проверяем подключение
    db = SessionLocal()
    try:
        # Простая проверка подключения
        categories_count = len(crud.get_all_categories(db))
        books_count = len(crud.get_all_books(db))
        print(f"✅ Подключение установлено")
        print(f"📚 В базе: {categories_count} категорий, {books_count} книг")
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        print("⚠️  Возможно, база данных не инициализирована.")
        print("   Запустите сначала: python app/init_db.py")
        exit(1)
    finally:
        db.close()
    
    # Запускаем главное меню
    main_menu()
EOFcat > app/main.py << 'EOF'
"""
Основной модуль приложения для работы с базой данных
"""
import sys
import os
from tabulate import tabulate

# Добавляем корневую директорию в путь Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.db import SessionLocal
from app.db import crud


def display_categories():
    """Отображает все категории"""
    db = SessionLocal()
    try:
        categories = crud.get_all_categories(db)
        
        print("=" * 60)
        print("📚 КАТЕГОРИИ КНИГ")
        print("=" * 60)
        
        if not categories:
            print("Категории не найдены")
            return
        
        # Формируем данные для таблицы
        table_data = []
        for category in categories:
            books_count = len(crud.get_books_by_category(db, category.id))
            table_data.append([
                category.id,
                category.title,
                books_count
            ])
        
        # Выводим таблицу
        headers = ["ID", "Название категории", "Кол-во книг"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        print()
        
    finally:
        db.close()


def display_books():
    """Отображает все книги с информацией о категориях"""
    db = SessionLocal()
    try:
        books_with_categories = crud.get_books_with_categories(db)
        
        print("=" * 60)
        print("📖 ВСЕ КНИГИ")
        print("=" * 60)
        
        if not books_with_categories:
            print("Книги не найдены")
            return
        
        # Формируем данные для таблицы
        table_data = []
        for book in books_with_categories:
            table_data.append([
                book["book_id"],
                book["book_title"],
                f'{book["book_price"]:.2f} руб.',
                book["category_title"],
                (book["book_description"][:50] + "...") if book["book_description"] and len(book["book_description"]) > 50 else book["book_description"]
            ])
        
        # Выводим таблицу
        headers = ["ID", "Название книги", "Цена", "Категория", "Описание (первые 50 символов)"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        print()
        
    finally:
        db.close()


def display_books_by_category(category_id: int):
    """Отображает книги определенной категории"""
    db = SessionLocal()
    try:
        category = crud.get_category(db, category_id)
        if not category:
            print(f"❌ Категория с ID {category_id} не найдена")
            return
        
        books = crud.get_books_by_category(db, category_id)
        
        print("=" * 60)
        print(f"📚 КНИГИ В КАТЕГОРИИ: {category.title}")
        print("=" * 60)
        
        if not books:
            print("Книги не найдены")
            return
        
        # Формируем данные для таблицы
        table_data = []
        for book in books:
            table_data.append([
                book.id,
                book.title,
                f'{book.price:.2f} руб.',
                (book.description[:60] + "...") if book.description and len(book.description) > 60 else book.description
            ])
        
        # Выводим таблицу
        headers = ["ID", "Название", "Цена", "Описание"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        print()
        
    finally:
        db.close()


def display_statistics():
    """Отображает статистику базы данных"""
    db = SessionLocal()
    try:
        categories = crud.get_all_categories(db)
        all_books = crud.get_all_books(db)
        
        print("=" * 60)
        print("📊 СТАТИСТИКА БАЗЫ ДАННЫХ")
        print("=" * 60)
        
        print(f"Всего категорий: {len(categories)}")
        print(f"Всего книг: {len(all_books)}")
        print()
        
        print("📈 Распределение книг по категориям:")
        print("-" * 40)
        
        stats_data = []
        for category in categories:
            books_in_category = crud.get_books_by_category(db, category.id)
            stats_data.append([
                category.title,
                len(books_in_category),
                f"{(len(books_in_category) / len(all_books) * 100):.1f}%"
            ])
        
        headers = ["Категория", "Кол-во книг", "Процент"]
        print(tabulate(stats_data, headers=headers, tablefmt="simple"))
        print()
        
        # Самая дорогая и дешевая книга
        if all_books:
            most_expensive = max(all_books, key=lambda x: x.price)
            cheapest = min(all_books, key=lambda x: x.price)
            
            print("💰 Интересные факты:")
            print(f"  Самая дорогая книга: '{most_expensive.title}' - {most_expensive.price:.2f} руб.")
            print(f"  Самая дешевая книга: '{cheapest.title}' - {cheapest.price:.2f} руб.")
            print(f"  Средняя цена: {sum(b.price for b in all_books) / len(all_books):.2f} руб.")
        
    finally:
        db.close()


def search_books_interactive():
    """Интерактивный поиск книг"""
    db = SessionLocal()
    try:
        print("🔍 ПОИСК КНИГ")
        print("-" * 40)
        
        search_term = input("Введите название или часть описания для поиска: ").strip()
        
        if not search_term:
            print("❌ Поисковый запрос не может быть пустым")
            return
        
        books = crud.search_books(db, search_term)
        
        print(f"\n📖 Найдено книг: {len(books)}")
        
        if books:
            table_data = []
            for book in books:
                category = crud.get_category(db, book.category_id)
                table_data.append([
                    book.id,
                    book.title,
                    f'{book.price:.2f} руб.',
                    category.title if category else "Неизвестно",
                    (book.description[:50] + "...") if book.description and len(book.description) > 50 else book.description
                ])
            
            headers = ["ID", "Название", "Цена", "Категория", "Описание"]
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
        else:
            print("Книги по вашему запросу не найдены")
        
        print()
        
    finally:
        db.close()


def main_menu():
    """Главное меню приложения"""
    while True:
        print("\n" + "=" * 60)
        print("📚 СИСТЕМА УПРАВЛЕНИЯ БИБЛИОТЕКОЙ")
        print("=" * 60)
        print("1. Показать все категории")
        print("2. Показать все книги")
        print("3. Показать книги по категории")
        print("4. Показать статистику")
        print("5. Поиск книг")
        print("6. Выйти")
        print("-" * 60)
        
        choice = input("Выберите действие (1-6): ").strip()
        
        if choice == "1":
            display_categories()
        elif choice == "2":
            display_books()
        elif choice == "3":
            try:
                category_id = int(input("Введите ID категории: "))
                display_books_by_category(category_id)
            except ValueError:
                print("❌ Ошибка: введите число")
        elif choice == "4":
            display_statistics()
        elif choice == "5":
            search_books_interactive()
        elif choice == "6":
            print("👋 До свидания!")
            break
        else:
            print("❌ Неверный выбор. Попробуйте снова.")
        
        input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    # Устанавливаем tabulate, если его нет
    try:
        import tabulate
    except ImportError:
        print("Установка необходимой библиотеки tabulate...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "tabulate"])
        import tabulate
    
    print("🚀 Запуск системы управления библиотекой")
    print("📊 Подключение к базе данных...")
    
    # Проверяем подключение
    db = SessionLocal()
    try:
        # Простая проверка подключения
        categories_count = len(crud.get_all_categories(db))
        books_count = len(crud.get_all_books(db))
        print(f"✅ Подключение установлено")
        print(f"📚 В базе: {categories_count} категорий, {books_count} книг")
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        print("⚠️  Возможно, база данных не инициализирована.")
        print("   Запустите сначала: python app/init_db.py")
        exit(1)
    finally:
        db.close()
    
    # Запускаем главное меню
    main_menu()
