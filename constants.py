"""
Константы приложения
"""
from os import getenv

try:
    import dotenv
    dotenv.load_dotenv(".env")
except ImportError:
    pass

# Telegram API
API_ID = getenv("API_ID")
API_HASH = getenv("API_HASH")

# DB
DB_HOST = getenv("DB_HOST")
DB_PORT = getenv("DB_PORT")
DB_SECRET = getenv("DB_SECRET")
DB_USERNAME = getenv("DB_USERNAME")
DB_NAME = getenv("DB_NAME")

# Settings
SLEEP_DELAY = 10

# Misc
RANDOM_IMG_SERVICE = "https://picsum.photos/"  # Случайные изображения