"""
Модуль с CRUD операциями для базы данных
"""
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from app.db import models


# ========== CRUD для категорий ==========

def create_category(db: Session, title: str) -> models.Category:
    """
    Создает новую категорию
    """
    db_category = models.Category(title=title)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_category(db: Session, category_id: int) -> Optional[models.Category]:
    """
    Получает категорию по ID
    """
    return db.query(models.Category).filter(models.Category.id == category_id).first()


def get_category_by_title(db: Session, title: str) -> Optional[models.Category]:
    """
    Получает категорию по названию
    """
    return db.query(models.Category).filter(models.Category.title == title).first()


def get_all_categories(db: Session, skip: int = 0, limit: int = 100) -> List[models.Category]:
    """
    Получает все категории с пагинацией
    """
    return db.query(models.Category).offset(skip).limit(limit).all()


def update_category(db: Session, category_id: int, title: str) -> Optional[models.Category]:
    """
    Обновляет категорию
    """
    db_category = get_category(db, category_id)
    if db_category:
        db_category.title = title
        db.commit()
        db.refresh(db_category)
    return db_category


def delete_category(db: Session, category_id: int) -> bool:
    """
    Удаляет категорию по ID
    """
    db_category = get_category(db, category_id)
    if db_category:
        db.delete(db_category)
        db.commit()
        return True
    return False


# ========== CRUD для книг ==========

def create_book(
    db: Session,
    title: str,
    price: float,
    category_id: int,
    description: Optional[str] = None,
    url: Optional[str] = None
) -> models.Book:
    """
    Создает новую книгу
    """
    db_book = models.Book(
        title=title,
        description=description,
        price=price,
        url=url,
        category_id=category_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_book(db: Session, book_id: int) -> Optional[models.Book]:
    """
    Получает книгу по ID
    """
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def get_all_books(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    category_id: Optional[int] = None
) -> List[models.Book]:
    """
    Получает все книги с пагинацией и фильтрацией по категории
    """
    query = db.query(models.Book)
    
    if category_id:
        query = query.filter(models.Book.category_id == category_id)
    
    return query.offset(skip).limit(limit).all()


def update_book(
    db: Session,
    book_id: int,
    **kwargs
) -> Optional[models.Book]:
    """
    Обновляет книгу
    """
    db_book = get_book(db, book_id)
    if db_book:
        for key, value in kwargs.items():
            if hasattr(db_book, key) and value is not None:
                setattr(db_book, key, value)
        db.commit()
        db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int) -> bool:
    """
    Удаляет книгу по ID
    """
    db_book = get_book(db, book_id)
    if db_book:
        db.delete(db_book)
        db.commit()
        return True
    return False


def get_books_by_category(db: Session, category_id: int) -> List[models.Book]:
    """
    Получает все книги определенной категории
    """
    return db.query(models.Book).filter(models.Book.category_id == category_id).all()


def search_books(db: Session, search_term: str) -> List[models.Book]:
    """
    Ищет книги по названию или описанию
    """
    return db.query(models.Book).filter(
        (models.Book.title.ilike(f"%{search_term}%")) | 
        (models.Book.description.ilike(f"%{search_term}%"))
    ).all()


# ========== Утилиты ==========

def get_books_with_categories(db: Session) -> List[Dict[str, Any]]:
    """
    Получает все книги с информацией о категориях
    """
    results = db.query(models.Book, models.Category).join(models.Category).all()
    
    books_with_categories = []
    for book, category in results:
        books_with_categories.append({
            "book_id": book.id,
            "book_title": book.title,
            "book_price": book.price,
            "book_description": book.description,
            "category_id": category.id,
            "category_title": category.title
        })
    
    return books_with_categories
