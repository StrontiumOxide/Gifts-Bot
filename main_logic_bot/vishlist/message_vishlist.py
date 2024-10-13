from aiogram import Router, types as tp
from aiogram.filters import Command
from main_logic_bot.vishlist import kb_vishlist as kb

router = Router(name='message_vishlist')


@router.message(Command(commands=['get_vishlist']))
async def vishlist_handler(message: tp.Message) -> None:
    """Функция по обработке команды /get_vishlist"""

    text = f'''
Итак, что ты собираешься сделать? 🧐

Узнать, что хочет твоя половинка? 👀  
Или, возможно, вспомнить, что уже есть в твоём виш-листе? 😉

Не забывай: ты всегда можешь добавить что-то новое или удалить лишнее! 🌟
'''

    await message.answer(
        text=text,
        reply_markup=kb.inline.create_select_vish(user_id=message.from_user.id)
    )
