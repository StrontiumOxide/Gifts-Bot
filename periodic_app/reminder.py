from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from random import randint, choice
from utils.loader_token import Token
from functions.sqlite_work import BD
from main_logic_bot.vishlist import kb_vishlist as kb


def select_message(gift: tuple) -> str:
    """Функция по выбору текста для ответа"""

    phrases = [
        f'В дату <b>"{gift[5]}"</b> ваша вторая половинка загадала желание <b>"{gift[2]}"</b>. Не забудьте об этом, это крайне важно!',
        f'<b>"{gift[5]}"</b> — именно в этот момент ваша вторая половинка создала желание <b>"{gift[2]}"</b>. Убедитесь, что вы помните об этом!',
        f'Не упустите из виду желание вашей второй половинки <b>"{gift[2]}"</b>, которое было загадано <b>"{gift[5]}"</b>!',
        f'Вашей второй половинке так важна <b>"{gift[2]}"</b> — это желание было создано <b>"{gift[5]}"</b>. Обязательно помните об этом!',
        f'Ваша вторая половинка <b>"{gift[5]}"</b> создала желание <b>"{gift[2]}"</b>. Постарайтесь не забыть об этом!',
        f'Помните, что <b>"{gift[5]}"</b> ваша вторая половинка загадала желание <b>"{gift[2]}"</b>. Это очень важно!',
        f'<b>"{gift[5]}"</b> — ваша вторая половинка выразила желание <b>"{gift[2]}"</b>. Не забудьте об этом!',
        f'В момент <b>"{gift[5]}"</b> ваша вторая половинка создала желание <b>"{gift[2]}"</b>. Это важно!',
        f'Неприятные последствия, если вы забудете о желании <b>"{gift[2]}"</b>, созданном вашей второй половинкой <b>"{gift[5]}"</b>!',
        f'Зафиксируйте в памяти, что <b>"{gift[5]}"</b> ваша вторая половинка загадала желание <b>"{gift[2]}"</b>.',
        f'Напоминаем вам о желании вашей второй половинки — <b>"{gift[2]}"</b>, загаданный <b>"{gift[5]}"</b>. Не забудьте об этом!',
        f'Не прозевайте: <b>"{gift[5]}"</b> — ваша вторая половинка создала желание <b>"{gift[2]}"</b>. Это очень важно!',
        f'Ваше внимание требуется: <b>"{gift[5]}"</b> ваша вторая половинка загадала желание <b>"{gift[2]}"</b>.',
        f'Имейте в виду, что в дату <b>"{gift[5]}"</b> ваша вторая половинка создала желание <b>"{gift[2]}"</b>. Это важно!'
    ]

    text = f'''
{choice(phrases)}

<b><a href='{gift[4]}'>Ссылка на товар 🔗</a></b>
'''
    return text


async def send_reminder(bot: Bot) -> None:
    """Функция, которая отправляет напоминание о желаниях"""

    list_users = [Token(key='HIS_ID').find(), Token(key='HER_ID').find()]
    for user_id in list_users:

        if user_id == list_users[0]:
            half_id = list_users[1]
        else:
            half_id = list_users[0]

        data = await BD(path='gift.sqlite3').get_gifts(user_id=user_id)

        if (randint(1, 5) == 1) and (len(data) != 0):
            gift = choice(data)

            text = select_message(gift=gift)

            try:
                await bot.send_message(
                    chat_id=half_id,
                    text=text,
                    reply_markup=kb.inline.create_select_vish(user_id=half_id)
                )
            except (TelegramBadRequest, TelegramForbiddenError):
                pass
