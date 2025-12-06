"""
Модуль с моделями SQLAlchemy для базы данных
"""
from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.db import Base


class Category(Base):
    """
    Модель категорий книг
    """
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(100), nullable=False, unique=True, index=True)

    # Связь один-ко-многим с книгами
    books = relationship("Book", back_populates="category", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Category(id={self.id}, title='{self.title}')>"


class Book(Base):
    """
    Модель книг
    """
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    url = Column(String(500), nullable=True)
    
    # Внешний ключ на категорию
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)

    # Связь многие-к-одному с категорией
    category = relationship("Category", back_populates="books")

    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', price={self.price})>"
