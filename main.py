import asyncio
from tele_utils import bot, dp, start_bot, stop_bot
from lead_handler import check_and_handle_leads

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger


async def periodic_lead_check():
    while True:
        await check_and_handle_leads()
        await asyncio.sleep(3)  # Проверка каждые 3 секунды


async def main():
    await start_bot()
    scheduler = AsyncIOScheduler()

    # Планировщик для ежедневного отчета
    scheduler.add_job(
        check_and_handle_leads,
        CronTrigger(hour=8, minute=0),  # Ежедневно в 08:00
        id="daily_report"
    )

    scheduler.start()
    try:
        await periodic_lead_check()
    finally:
        await stop_bot()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен.")
