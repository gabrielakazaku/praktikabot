"""
Модуль для работы с подключением к базе данных PostgreSQL
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Получаем параметры подключения из переменных окружения
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "octagon_db")
DB_USER = os.getenv("DB_USER", "octagon")
DB_PASSWORD = os.getenv("DB_PASSWORD", "12345")

# Формируем строку подключения
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Создаем движок SQLAlchemy
engine = create_engine(DATABASE_URL, echo=True)  # echo=True для логгирования SQL-запросов

# Создаем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()


def get_db():
    """
    Функция-генератор для получения сессии базы данных.
    Используется для dependency injection в FastAPI.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """
    Создает все таблицы в базе данных на основе моделей.
    """
    Base.metadata.create_all(bind=engine)
    print("✅ Таблицы успешно созданы!")


def drop_tables():
    """
    Удаляет все таблицы из базы данных.
    Используйте с осторожностью!
    """
    Base.metadata.drop_all(bind=engine)
    print("⚠️ Таблицы удалены!")


# Проверка подключения при импорте модуля
if __name__ == "__main__":
    try:
        with engine.connect() as conn:
            print(f"✅ Подключение к базе данных {DB_NAME} успешно!")
            print(f"📊 URL: {DATABASE_URL}")
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
