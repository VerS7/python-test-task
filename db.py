"""
Работа с БД
"""
from datetime import datetime

from constants import DB_USERNAME, DB_HOST, DB_NAME, DB_PORT, DB_SECRET

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import (Column, Integer, String, DateTime)
from sqlalchemy.orm import declarative_base


connection_string = URL.create(
  'postgresql+asyncpg',
  username=DB_USERNAME,
  password=DB_SECRET,
  host=DB_HOST,
  port=DB_PORT,
  database=DB_NAME,
)

engine = create_async_engine(
    connection_string,
    echo=True,
    future=True
)

Base = declarative_base()


class RegisteredUser(Base):
    """
    Таблица с пользователями и временем регистрации
    """
    __tablename__ = "RegisteredUsers"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, unique=True, index=True)
    username = Column(String, index=True)
    registered_at = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(bind=engine)
