import os
import time
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

start_time = time.time()
uptime_router = Router()

async def start_bot():
    print("Бот запущен.")

async def stop_bot():
    await bot.session.close()
    print("Бот остановлен.")

@uptime_router.message(F.text == "/status")
async def cmd_status(message: Message):
    uptime = time.time() - start_time
    hours, remainder = divmod(int(uptime), 3600)
    minutes, _ = divmod(remainder, 60)
    await message.answer(f"⏱ Бот работает уже {hours}ч {minutes}мин")

async def notify_new_lead(lead):
    msg = (
        f"📌 Лид №{lead['id']} принят!
"
        f"👤 {lead['name']}
"
        f"🏙️ {lead['object']}
"
        f"📅 {lead['date']}
"
        f"🛰️ Источник: {lead['source']}
"
        f"🔗 {lead['link']}"
    )
    await bot.send_message(chat_id=CHAT_ID, text=msg)