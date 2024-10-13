from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start_link = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Нажми меня ⬇️', callback_data='click')
        ]
    ]
)
