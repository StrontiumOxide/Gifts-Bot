from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

remove = ReplyKeyboardRemove()

yes_no = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Да ✅'),
            KeyboardButton(text='Нет ❌')
        ]
    ],
    resize_keyboard=True
)

cancel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Завершить ✋')
        ]
    ],
    resize_keyboard=True
)
