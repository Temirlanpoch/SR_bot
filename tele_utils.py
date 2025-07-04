import logging
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from datetime import datetime, timezone, timedelta
import os

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")  # Куда отправлять уведомления

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

# Стартовое время запуска
start_time = datetime.now(timezone(timedelta(hours=5)))

async def notify_new_lead(lead: dict, missed=False):
    status = "❌ <b>УПУЩЕН</b>" if missed else "📌 Лид принят"
    comment = lead.get("comment", "—")

    text = (
        f"{status} №<b>{lead['id']}</b>\n"
        f"👤 <b>{lead['client']}</b>\n"
        f"🏙️ <b>{lead['apartment']}</b>\n"
        f"📅 <b>{lead['date']}</b>\n"
        f"🛰️ Источник: <b>{lead['source']}</b>\n"
        f"💬 Комментарий: <i>{comment}</i>\n"
        f"🔗 <a href='https://crm.smartremont.kz/deal/{lead['id']}'>Открыть в CRM</a>"
    )

    try:
        await bot.send_message(chat_id=CHAT_ID, text=text)
    except Exception as e:
        logging.error(f"Ошибка при отправке уведомления: {e}")

async def send_status():
    now = datetime.now(timezone(timedelta(hours=5)))
    diff = now - start_time
    hours, remainder = divmod(diff.total_seconds(), 3600)
    minutes = remainder // 60
    uptime = f"{int(hours)} ч {int(minutes)} мин"

    msg = (
        f"🟢 Бот активен!\n"
        f"⏱️ Аптайм: <b>{uptime}</b>\n"
        f"🚀 Старт был: <b>{start_time.strftime('%H:%M:%S')}</b>"
    )

    await bot.send_message(chat_id=CHAT_ID, text=msg)

async def start_bot():
    logging.info("Запуск бота...")

async def stop_bot():
    logging.info("Остановка бота...")
    await bot.session.close()
