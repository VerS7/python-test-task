"""
App
"""
import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message

from loguru import logger

from constants import API_ID, API_HASH
from db import RegisteredUser, AsyncSessionLocal, meta_create, select


app = Client("ThisAccount", API_ID, API_HASH)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(meta_create())
    app.run()
