from aiogram import Router, types as tp, F

router = Router(name='callback_query_greetings')


@router.callback_query(F.data == 'click')
async def start_link_handler(callback_query: tp.CallbackQuery) -> None:
    """ Функция по обработке data="click" """

    await callback_query.answer(
        text='Я рад, что вы нажали на кнопку 😊',
        show_alert=True
    )
  