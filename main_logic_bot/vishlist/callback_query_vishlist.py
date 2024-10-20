from aiogram import Router, types as tp, F
from main_logic_bot.vishlist import kb_vishlist as kb
from utils.loader_token import Token
from functions.sqlite_work import BD

router = Router(name='callback_query_vishlist')


@router.callback_query(F.data == 'my')
async def callback_my_vishlist(callback_query: tp.CallbackQuery) -> None:
    """Функция по обработке команды callback_data = my"""

    text = f'''
Здесь представлены все твои хотелки и пожелания. 🌟 

Чтобы узнать более подробную информацию, выбери желание. 📖 

Также здесь ты можешь создать свою новую хотелку. ✨
'''

    await callback_query.message.edit_text(
        text=text,
        reply_markup= await kb.inline.create_list_gifts(user_id=callback_query.from_user.id, slice=0)
    )


@router.callback_query(F.data == 'strange')
async def callback_strange_vishlist(callback_query: tp.CallbackQuery) -> None:
    """Функция по обработке команды callback_data = strange"""

    if callback_query.from_user.id == int(Token(key='HIS_ID').find()):
        user_id = Token(key='HER_ID').find()
    else:
        user_id = Token(key='HIS_ID').find()


    text = f'''
А здесь представлены желания твоей второй половинки. 🎁

Изменять их ты не сможешь 😔

Загляни скорее внутрь и сделай подарок как можно скорее! 🎀✨
'''

    await callback_query.message.edit_text(
        text=text,
        reply_markup= await kb.inline.create_list_gifts(user_id=int(user_id), slice=1)
    )


@router.callback_query(lambda call: 'gift_id' in call.data)
async def callback_in_gift_id(callback_query: tp.CallbackQuery) -> None:
    """Функция по отображению желания"""

    gift_id = int(callback_query.data.split(sep='_')[-1])
    data = await BD(path='gift.sqlite3').get_gift(gift_id=gift_id)
    data = data[0]

    text = f'''
<b>[{data[5]}]</b>

Наименование 🌟: <b>"{data[2]}"</b>

Послание 💌: <i>"{data[3]}"</i>

<b><a href='{data[4]}'>Ссылка на товар 🔗</a></b>
'''
    
    if data[1] == callback_query.from_user.id:
        status = True
    else:
        status = False

    await callback_query.message.edit_text(
        text=text,
        reply_markup=kb.inline.create_kb_for_delete(gift_id=int(data[0]), permission_delete=status)
    )
    

@router.callback_query(lambda call: 'delete_gift' in call.data)
async def callback_in_delete_gift(callback_query: tp.CallbackQuery) -> None:
    """Функция по уточнения удаления желания"""

    gift_id = int(callback_query.data.split(sep='_')[-1])
    data = await BD(path='gift.sqlite3').get_gift(gift_id=gift_id)
    data = data[0]

    text = f'''
Вы точно хотите удалить желание: <b>"{data[2]}"</b>?
'''
    
    await callback_query.message.edit_text(
        text=text,
        reply_markup=kb.inline.create_delete(gift_id=gift_id)
    )


@router.callback_query(lambda call: 'yes_delete' in call.data)
async def callback_in_delete_gift(callback_query: tp.CallbackQuery) -> None:
    """Функция по удалению желания"""

    gift_id = int(callback_query.data.split(sep='_')[-1])
    await BD(path='gift.sqlite3').delete_gift(gift_id=gift_id)
    
    await callback_query.answer(
        text='Желание успешно удалено',
        show_alert=True
    )

    text = f'''
Здесь представлены все твои хотелки и пожелания. 🌟 

Чтобы узнать более подробную информацию, выбери желание. 📖 

Также здесь ты можешь создать свою новую хотелку. ✨
'''
    
    await callback_query.message.edit_text(
        text=text,
        reply_markup= await kb.inline.create_list_gifts(user_id=callback_query.from_user.id, slice=0)
    )


@router.callback_query(F.data == 'back')
async def callback_back_vishlist(callback_query: tp.CallbackQuery) -> None:
    """Функция по обработке команды callback_data = back"""

    text = f'''
Итак, что ты собираешься сделать? 🧐

Узнать, что хочет твоя половинка? 👀  
Или, возможно, вспомнить, что уже есть в твоём виш-листе? 😉

Не забывай: ты всегда можешь добавить что-то новое или удалить лишнее! 🌟
'''
    
    await callback_query.message.edit_text(
        text=text,
        reply_markup= kb.inline.create_select_vish(user_id=callback_query.from_user.id)
    )
