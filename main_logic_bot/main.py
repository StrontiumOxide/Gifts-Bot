from aiogram import Bot, Dispatcher
from utils.commands_bot import set_commands

from utils.middlewares import CountMiddleware, StopStrangerMiddleware
from main_logic_bot.greetings import message_greetings


async def main_polling(bot: Bot, dp: Dispatcher) -> None:
    """Функция, отвечающая за polling"""

        # Подключение Middleware
    dp.update.outer_middleware(CountMiddleware())
    dp.message.outer_middleware(StopStrangerMiddleware())

        # Список с модулями Telegram-бота
    list_modules = [

            # Приветствие
        message_greetings

    ]

        # Подключение модулей
    dp.include_routers(*map(lambda file: file.router, list_modules))

        # Подключение командного меню
    await set_commands(bot=bot)

        # Удаление webhook
    await bot.delete_webhook(drop_pending_updates=True)
    
        # Polling
    await dp.start_polling(bot, polling_timeout=20)
