"""
App
"""
import asyncio

from typing import List, Union, BinaryIO
from random import randint
from datetime import datetime, timedelta

from pyrogram import Client, filters
from pyrogram.types import Message

from loguru import logger

from constants import API_ID, API_HASH, SLEEP_DELAY, RANDOM_IMG_SERVICE
from db import RegisteredUser, AsyncSessionLocal, meta_create, select

app = Client("ThisAccount", API_ID, API_HASH)


async def send_message(chat_id: int, text: str) -> None:
    """Отправляет сообщение по chat_id"""
    try:
        await app.send_message(chat_id, text)
        logger.info(f"Сообщение отправлено. ChatID: {chat_id}: Text: {text}")
    except Exception as e:
        logger.error(f"Ошибка отправки сообщения. ChatID: {chat_id}", e=e)


async def send_photo(chat_id: str, image: Union[str, BinaryIO]) -> None:
    """Отправляет изображение по chat_id"""
    try:
        await app.send_photo(chat_id, image)
        logger.info(f"Изображение отправлено. ChatID: {chat_id}")
    except Exception as e:
        logger.error(f"Ошибка отправки изображения. ChatID: {chat_id}", e=e)


async def register_user(chat_id: int, username: str):
    """Регистрирует пользователя в БД"""
    user = RegisteredUser(chat_id=chat_id, username=username)
    async with AsyncSessionLocal() as session:
        session.add(user)
        await session.commit()
    logger.info(f"Пользователь {username} ChatID: {chat_id} зарегистрирован.")


async def get_users() -> List[RegisteredUser]:
    """Возвращает список пользователей из БД"""
    async with AsyncSessionLocal() as session:
        response = await session.execute(select(RegisteredUser))
    return [user[0] for user in response.fetchall()]


async def get_users_today() -> List[RegisteredUser]:
    """Возвращает пользователей, добавленных сегодня"""
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    async with AsyncSessionLocal() as session:
        response = await session.execute(select(RegisteredUser)
                                         .filter(RegisteredUser.registered_at >= today))
    return [user[0] for user in response.fetchall()]


async def check_trigger(chat_id: int) -> bool:
    """Проверяет, есть ли в истории сообщений триггерное сообщение"""
    async for msg in app.get_chat_history(chat_id, limit=1000):
        if msg.from_user.is_self and "Хорошего дня" in msg.text:
            return True
        return False


def compare_time(time_value: datetime, tolerance_s: int = 30) -> bool:
    """Сравнивает time_value с текущим временем с заданной погрешностью"""
    time_difference = abs((time_value - datetime.now()).total_seconds())
    return time_difference <= tolerance_s


@app.on_message(filters.command("users_today") & filters.private)
async def users_today_command(_, message: Message):
    users_ = [f"**User: {user.username} Chat ID: {user.chat_id}**\n" for user in await get_users_today()]
    await message.reply(f"Пользователей за сегодня: {len(users_)}\n{''.join(users_)}")


@app.on_message(filters.text & filters.private)
async def on_user_message(_, message: Message):
    chat_id = message.chat.id
    username = message.from_user.username if message.from_user.username else "Unknown"

    async with AsyncSessionLocal() as session:
        response = await session.execute(select(RegisteredUser).filter(RegisteredUser.chat_id == chat_id))
        user = response.scalar()
        if not user:
            await register_user(chat_id, username)


async def main():
    """ main """
    await meta_create()  # Создание БД при необходимости
    async with app:
        while True:
            for user in await get_users():
                if compare_time(user.registered_at + timedelta(minutes=10)):
                    await send_message(user.chat_id, "Добрый день!")

                elif compare_time(user.registered_at + timedelta(minutes=90)):
                    await send_message(user.chat_id, "Подготовила для вас материал")
                    await app.send_photo(user.chat_id, RANDOM_IMG_SERVICE +
                                         f"{randint(200, 1000)}/{randint(200, 1000)}")

                elif compare_time(user.registered_at + timedelta(hours=2)) and check_trigger(user.chat_id):
                    await send_message(user.chat_id, "Скоро вернусь с новым материалом!")
            await asyncio.sleep(SLEEP_DELAY)


if __name__ == '__main__':
    try:
        app.run(main())
    except KeyboardInterrupt:
        logger.info("Выход из приложения.")
