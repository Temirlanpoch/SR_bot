import asyncio
import os
from dotenv import load_dotenv
from tele_utils import bot, dp, start_bot, stop_bot, uptime_router
from lead_handler import check_and_handle_leads
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

load_dotenv()

scheduler = AsyncIOScheduler()
scheduler.start()


async def periodic_check():
    while True:
        await check_and_handle_leads()
        await asyncio.sleep(30)

async def main():
    await start_bot()
    asyncio.create_task(periodic_check())
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        asyncio.run(stop_bot())
