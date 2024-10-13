import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from utils.loader_token import Token

from main_logic_bot.main import main_polling
from periodic_app.main import planned_machine

logging.basicConfig(level=logging.ERROR, filename='bot_log.log', filemode='a', encoding='utf-8')


async def main():
    """Главная функция"""

    bot = Bot(token=Token(key='TELEGRAM').find(), parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    try:
            # Уведомление о запуске Telegram-бота
        await bot.send_message(
            chat_id=Token(key='MY_ID').find(),
            text='<b>[INFO] Telegram-бот запущен!</b>'
        )
    except Exception:
        print('[INFO] Telegram-бот запущен!')

        # Сбор всех корутин
    await asyncio.gather(
        main_polling(bot=bot, dp=dp),
        planned_machine()
    )


if __name__ == "__main__":
    asyncio.run(main())
