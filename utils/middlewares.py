from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import Update
from utils.config import limit_request, max_requests


class CountMiddleware(BaseMiddleware):
    """Middleware по счёту апдейтов"""

    async def __call__(self, handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]], event: Update, data: Dict[str, Any]) -> Any:
        
        if event.message:
            user_id = event.message.from_user.id
            username = event.message.from_user.full_name

        elif event.callback_query:
            user_id = event.callback_query.from_user.id
            username = event.callback_query.from_user.full_name

        if user_id in limit_request:
            limit_request[user_id]['count'] += 1
        else:
            limit_request[user_id] = {'count': 1, 'status': True}

            # Выполнение соответствующего хендлера
        if limit_request[user_id]['count'] > max_requests:
            if limit_request[user_id]['status']:
                limit_request[user_id]['status'] = False
                text = f'''
⚠️ <b>ВНИМАНИЕ</b> ⚠️

<b>от API Telegram</b>
<blockquote>Уважаемый, <b>{username}</b>❗️
Вы превысили лимит по запросам 💭
Повторите пожалуйста позже ⏳
</blockquote>
'''
                await event.message.answer(
                    text=text
                )
            return
        
        await handler(event, data)
