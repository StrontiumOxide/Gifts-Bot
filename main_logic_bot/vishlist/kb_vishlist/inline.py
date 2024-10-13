from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.loader_token import Token


def create_select_vish(user_id: int) -> InlineKeyboardMarkup:
    """Функция по создании персонализированной клавиатуры"""

    envirion_user_id = Token(key='HIS_ID').find()
    if str(user_id) == envirion_user_id:
        btn_text = 'Её 💝'
        call_data = f'stranger_{envirion_user_id}'
    else:
        btn_text = 'Его 💝'
        call_data = f'stranger_{envirion_user_id}'

    select_vish = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Моё 🎁', callback_data='my'),
                InlineKeyboardButton(text=btn_text, callback_data=call_data)
            ]
        ]
    )

    return select_vish
