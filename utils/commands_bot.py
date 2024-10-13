from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot) -> None:
    """Данная функция добавляет меню в бота с командами ниже"""

    commands = [
        BotCommand(
            command="start",
            description="Запуск бота ▶️"
        ),
        BotCommand(
            command="get_vishlist",
            description="Получить виш-лист 📋"
        )
    ]

    await bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())
