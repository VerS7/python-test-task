# Тествое задание
**Воронка начинается после первого сообщения от клиента.**
**Пояснение**: бот проверяет есть ли человек в БД, и если нет, то регистрирует его в БД и начинается воронка.

**Через какое время** / **Сообщения, которые отправляет с момента последнего**
_через 10 минут_ / Добрый день!
_через 90 минут_ / Подготовила для вас материал
_Сразу после_ / Отправка любого фото

_Через 2 часа если не найден в истории сообщений триггер "Хорошего дня" (от лица нашего аккаунта)_ / Скоро вернусь с новым материалом!

**Python** - ЯП 
**Sqlalchemy** (asyncpg) - для БД 
**Pyrogram** - для взаимодействия с Telegram API
**Loguru** - Логировать каждую успешную отправку сообщения

Сделать возможность просмотра кол-во зарегистрированный людей в БД за сегодня с помощью отправки команды ```/users_today``` в избранное аккаунта.
