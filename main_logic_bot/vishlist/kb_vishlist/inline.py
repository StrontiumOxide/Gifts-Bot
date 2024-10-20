from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from utils.loader_token import Token
from functions.sqlite_work import BD


def create_select_vish(user_id: int) -> InlineKeyboardMarkup:
    """Функция по создании персонализированной клавиатуры"""

    envirion_user_id = Token(key='HIS_ID').find()
    if str(user_id) == envirion_user_id:
        btn_text = 'Её 💝'
    else:
        btn_text = 'Его 💝'

    select_vish = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Моё 🎁', callback_data='my'),
                InlineKeyboardButton(text=btn_text, callback_data='strange')
            ]
        ]
    )

    return select_vish


async def create_list_gifts(user_id: int, slice: int) -> InlineKeyboardMarkup:
    """Функция по формированию списка подарков в виде клавиатуры"""

        # Подключение и запрос к БД
    data = await BD(path='gift.sqlite3').get_gifts(user_id=user_id)

        # Сортировка и создание inline-кнопок
    data.sort(key=lambda el: el[2])
    list_btn = map(lambda gift: InlineKeyboardButton(text=f'<< {gift[2]} >>', callback_data=f'gift_id_{gift[0]}'), data)

    list_back_kb = [
        InlineKeyboardButton(text='Создать ⚒️', callback_data='create_gift'),
        InlineKeyboardButton(text='Назад ⤴️', callback_data='back')
    ]

    kb = InlineKeyboardBuilder()
    kb.row(*list_btn, width=1)
    kb.row(*list_back_kb[slice:])

    return kb.as_markup()


def create_kb_for_delete(gift_id: int, permission_delete: bool = False) -> InlineKeyboardMarkup:
    """Функция по созданию клавиатуры для удаления"""

    kb = InlineKeyboardBuilder()

    list_delete_kb = [
        InlineKeyboardButton(text='Удалить 🚮', callback_data=f'delete_gift_{gift_id}'),
        InlineKeyboardButton(text='Назад ⤴️', callback_data='my')
    ]

    if not permission_delete:
        list_delete_kb = list_delete_kb[1:]
        list_delete_kb[0].callback_data = 'strange'

    kb.row(*list_delete_kb, width=2)

    return kb.as_markup()


def create_delete(gift_id: int) -> InlineKeyboardMarkup:
    """Функция по созданию клавиатуры для уточнения удаления"""

    kb = InlineKeyboardBuilder()
    kb.row(
        InlineKeyboardButton(text='Да ✅', callback_data=f'yes_delete_{gift_id}'),
        InlineKeyboardButton(text='Назад ⤴️', callback_data=f'gift_id_{gift_id}'),
        width=2
    )

    return kb.as_markup()
