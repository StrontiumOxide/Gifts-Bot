from aiogram import Router, types as tp, F
from aiogram.fsm.context import FSMContext
from datetime import datetime as dt
from utils.states import GiftState
from utils.loader_token import Token
from functions.sqlite_work import BD
from main_logic_bot.vishlist import kb_vishlist as kb

router = Router(name='message_vishlist_funnel')


async def check_text(message: tp.Message) -> bool | None:
    """Функция по проверке наличия текста в сообщении"""

    if not message.text:
        await message.answer(
            text='Извините, в вашем сообщении нет текста 😒',
            reply_markup=kb.reply.cancel
        )
        return True
    

async def check_content(message: tp.Message, state: FSMContext) -> bool | None:
    """Функция встречает ключевого слово и останавливает общение с ChatGPT"""

    text = f'''
Создание желание завершено ❗️
'''
    
    if message.text == 'Завершить ✋':
        await message.answer(
            text=text,
            reply_markup=kb.reply.remove
        )

        await state.clear()
        return True


@router.callback_query(F.data == 'create_gift')
async def callback_create_gift_vishlist(callback_query: tp.CallbackQuery, state: FSMContext) -> None:
    """Функция по обработке команды callback_data = create_gift"""

    text = f'''
Хорошо, начнём ☺️
Как будет называться твоё желание? 🌟
'''
    await state.clear()
    await callback_query.answer()
    await callback_query.message.answer(
        text=text,
        reply_markup=kb.reply.cancel
    )
    await state.set_state(GiftState.title)


@router.message(GiftState.title)
async def get_title(message: tp.Message, state: FSMContext) -> None:
    """Функция по получению наименования желания"""

        # Проверка наличия текста в сообщении
    if await check_text(message=message): return

        # Проверка на завершение общения
    if await check_content(message=message, state=state): return

    await state.update_data(title=message.text)

    text = f'''
<b>"{message.text}"</b> - прекрасное название 🌟
Что ж, теперь мне неоходимо чтобы ты написал(а) послание для своей второй половинки 💌
'''

    await message.answer(
            text=text,
            reply_markup=kb.reply.cancel
        )
    await state.set_state(GiftState.description)


@router.message(GiftState.description)
async def get_description(message: tp.Message, state: FSMContext) -> None:
    """Функция по получению послания"""

       # Проверка наличия текста в сообщении
    if await check_text(message=message): return

        # Проверка на завершение общения
    if await check_content(message=message, state=state): return

    await state.update_data(description=message.text)

    text = f'''
Ммм, какое послание 😍
Главное чтобы после такого все были счастливи и никто не упал в обморок ☠️

И последний шаг, я хочу получить ссылку на данный товар 🔗
'''
    
    await message.answer(
            text=text,
            reply_markup=kb.reply.cancel
        )
    await state.set_state(GiftState.link)


@router.message(GiftState.link)
async def get_link(message: tp.Message, state: FSMContext) -> None:
    """Функция по получению ссылки"""

       # Проверка наличия текста в сообщении
    if await check_text(message=message): return

        # Проверка на завершение общения
    if await check_content(message=message, state=state): return

    if 'https://' not in message.text:
        await message.answer(
            text='Извините, это не похоже на ссылку ❌',
            reply_markup=kb.reply.cancel
        )
        return

    await state.update_data(link=message.text)

    data: dict = await state.get_data()
    title = data.get('title')
    description = data.get('description')
    link = data.get('link')

    text = f'''
Все данные получены ✅
Вы точно хотите создать данное желание? 🧐
⬇️-⬇️-⬇️-⬇️-⬇️-⬇️-⬇️-⬇️-⬇️

Наименование 🌟: <b>"{title}"</b>

Послание 💌: <i>"{description}"</i>

<b><a href='{link}'>Ссылка на товар 🔗</a></b>
'''
    
    await message.answer(
            text=text,
            reply_markup=kb.reply.yes_no
        )
    await state.set_state(GiftState.status)


@router.message(GiftState.status)
async def get_status(message: tp.Message, state: FSMContext) -> None:
    """Функция по получению послания"""

       # Проверка наличия текста в сообщении
    if await check_text(message=message): return

    if message.text not in ['Да ✅', 'Нет ❌']:
        await message.answer(
            text='Мне нужен ответ <b>"Да ✅</b> или <b>"Нет ❌</b>',
        )
        return
    
    if  message.text == 'Нет ❌':
        await state.clear()
        await message.answer(
            text='Очень жаль, такое прекрасное желание было...',
            reply_markup=kb.reply.remove
        )
        return

    text = f'''
Желание успешно создано! ✅
Надеюсь ваша вторая половинка вам скоро его подарит! ☺️
'''
    
    await message.answer(
            text=text,
            reply_markup=kb.reply.remove
        )
    
    await save_gift(message=message, state=state)


async def save_gift(message: tp.Message, state: FSMContext) -> None:
    """Функция сохраняет желание и завершает диалог"""

    data: dict = await state.get_data()
    title = data.get('title')
    description = data.get('description')
    link = data.get('link')
    
        # Добавление записи в БД
    client_bd = BD(path='gift.sqlite3')
    await client_bd.add_gift(
        user_id=message.from_user.id,
        title=title,
        description=description,
        link=link,
        datetime=dt.now().strftime(r"%d.%m.%Y, %H:%M:%S")
    )

    await state.clear()

    await mail(message=message, title=title)


async def mail(message: tp.Message, title: str) -> None:
    """Уведомление второй половинки"""

    if message.from_user.id == int(Token(key='HIS_ID').find()):
        half_id = Token(key='HER_ID').find()
    else:
        half_id = Token(key='HIS_ID').find()

    await message.bot.send_message(
        chat_id=half_id,
        text=f'Ваша вторая половинка создала новое желание: <b>"{title}"</b>\nСкорее узнайте о нём больше информации 🤩'
    )
