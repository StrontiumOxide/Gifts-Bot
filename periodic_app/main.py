from apscheduler.schedulers.asyncio import AsyncIOScheduler
from periodic_app.clearing_request_limit import cleaner
from periodic_app.reminder import send_reminder
from utils.config import cleaning_frequency


async def planned_machine(**kwargs) -> None:
    """Функция по установке условий для периодических приложений"""

        # Инициализация класса
    scheduler = AsyncIOScheduler()

    scheduler.add_job(cleaner, 'interval', seconds=cleaning_frequency)
    scheduler.add_job(send_reminder, 'cron', hour=12, minute=0, args=[kwargs.get('bot')])

    scheduler.start()
