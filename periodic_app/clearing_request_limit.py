import asyncio

from utils.config import limit_request


async def cleaner() -> None:
    """Функция по очистке кеша запросов от пользователей"""

    limit_request.clear()

    await asyncio.sleep(1)
