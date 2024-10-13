from aiogram import Router, types as tp
from aiogram.filters import CommandStart
from main_logic_bot.greetings import kb_greetings as kb
from data.loader_file import load_file

router = Router(name='message_greetings')


@router.message(CommandStart())
async def start_handler(message: tp.Message) -> None:
    """Функция по обработке команды /start"""

    text = f'''
Привет, <b>{message.from_user.full_name}</b> 👋

<blockquote>Я представляю из себя базовый шаблон для написания Telegram-ботов на Aiogram 3</blockquote>
'''

    await message.answer_photo(
        photo=load_file(category='photo', filename='script.jpg'),
        caption=text,
        reply_markup=kb.inline.start_link
    )
