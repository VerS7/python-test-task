"""
Работа с изображениями
"""
import aiohttp

from loguru import logger


async def download_image(url: str) -> bytes:
    """Возвращает загруженное изображение в байтах"""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                return await response.read()
        except aiohttp.ClientResponseError as e:
            logger.error("Не удалось загрузить изображение.", e=e)
