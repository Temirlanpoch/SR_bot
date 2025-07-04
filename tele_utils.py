import time
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.markdown import hbold
from aiogram import Router

TOKEN = "8102338984:AAF6Qr6M-TCiNVzzQf9wLyZ_fkGOqgQLXKk"
ADMIN_CHAT_ID = "701350220"

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(storage=MemoryStorage())
uptime_router = Router()

# Засекаем время запуска
start_time = time.time()

# ⏱️ Команда /status
@uptime_router.message(F.text == "/status")
async def status_handler(message: Message):
    uptime_seconds = int(time.time() - start_time)
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    await message.reply(
        f"🤖 Бот работает уже: {hours}ч {minutes}м {seconds}с\n🕒 С {time.strftime('%d.%m.%Y %H:%M:%S', time.localtime(start_time))}"
    )

# 📥 Уведомление о принятом лиде
async def notify_new_lead(lead: dict):
    message = (
        f"📌 Лид №{lead['id']} принят!\n"
        f"👤 {lead['name']}\n"
        f"🏙️ {lead.get('housing_name', '—')} – КВ {lead.get('apartment_number', '—')}\n"
        f"📅 {lead.get('date', '—')}\n"
        f"🛰️ Источник: {lead.get('source', '—')}\n"
        f"💬 {lead.get('comment', 'Комментарий не указан')}\n"
        f"🔗 https://crm.smartremont.kz/deal/{lead['id']}"
    )
    await bot.send_message(ADMIN_CHAT_ID, message)

# ⚠️ Уведомление об упущенном лиде
async def notify_missed_lead(lead: dict):
    message = (
        f"⚠️ <b>Лид №{lead['id']} упущен!</b>\n"
        f"👤 {lead['name']}\n"
        f"🏙️ {lead.get('housing_name', '—')} – КВ {lead.get('apartment_number', '—')}\n"
        f"📅 {lead.get('date', '—')}\n"
        f"🛰️ Источник: {lead.get('source', '—')}\n"
        f"💬 {lead.get('comment', 'Комментарий не указан')}\n"
        f"🔗 https://crm.smartremont.kz/deal/{lead['id']}"
    )
    await bot.send_message(ADMIN_CHAT_ID, message)

# ❌ Уведомление об ошибке
async def notify_error(text: str):
    await bot.send_message(ADMIN_CHAT_ID, f"❌ Ошибка: {text}")

# 🔄 Запуск бота
async def start_bot():
    dp.include_router(uptime_router)
    await dp.start_polling(bot)

# ⛔ Остановка
async def stop_bot():
    await bot.session.close()
