from aiogram import Router, types as tp
from aiogram.filters import CommandStart

router = Router(name='message_greetings')


@router.message(CommandStart())
async def start_handler(message: tp.Message) -> None:
    """Функция по обработке команды /start"""

    text = f'''
Привет, <b>{message.from_user.full_name}</b> 👋

<blockquote>Быстрее взгляни на желания твоей половинки и сделай ей/ему неожиданный подарок! 🎁

Не забывай и о своих хотелках! 💖

Добавь всё, что ты хочешь, чтобы не упустить возможность получить то, о чём мечтаешь. ✨

Пусть ваши желания сбудутся и подарки будут особенно приятными! 🎉</blockquote>

Выбери команду <b>/get_vishlist</b>
'''

    await message.answer(
        text=text
    )
