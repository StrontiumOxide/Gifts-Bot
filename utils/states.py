from aiogram.fsm.state import State, StatesGroup


class GiftState(StatesGroup):
    """Класс для переменных подарка"""  

    title = State()
    description = State()
    link = State()
    status = State()
