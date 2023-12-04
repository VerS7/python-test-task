"""
Работа с БД
"""
from datetime import datetime

from constants import DB_USERNAME, DB_HOST, DB_NAME, DB_SECRET

from sqlalchemy import URL, MetaData
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import (Column, Integer, String, DateTime)
from sqlalchemy.orm import declarative_base

from loguru import logger


connection_string = URL.create(
  'postgresql+asyncpg',
  username=DB_USERNAME,
  password=DB_SECRET,
  host=DB_HOST,
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


AsyncSessionLocal = async_sessionmaker(engine, autocommit=False, autoflush=False)


async def meta_create():
    """Создаёт таблицы в БД по метаданным"""
    async with engine.begin() as conn:
        metadata = MetaData()
        await conn.run_sync(metadata.reflect)
        table_names = metadata.tables.keys()
        for table in reversed(Base.metadata.sorted_tables):
            if table not in table_names:
                logger.info(f"Таблица {table} уже существует.")
            else:
                await conn.run_sync(table.create)
                logger.info(f"Создана таблица {table}.")
