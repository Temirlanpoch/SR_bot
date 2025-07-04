import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

TELEGRAM_TOKEN = "8102338984:AAF6Qr6M-TCiNVzzQf9wLyZ_fkGOqgQLXKk"
TELEGRAM_CHAT_ID = "701350220"

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
scheduler = AsyncIOScheduler()
start_time = datetime.now()


async def send_lead_notification(lead: dict, missed: bool = False):
    status = "❌ Упущен лид" if missed else f"📌 Лид №{lead['id']} принят!"
    text = f"""\
{status}
👤 {lead.get('name', 'Неизвестно')}
🏙️ {lead.get('complex', 'Неизвестно')} – КВ {lead.get('flat', '–')}
📅 {lead.get('date', '—')}
🛰️ Источник: {lead.get('source', '—')}
💬 Комментарий: {lead.get('comment', '—')}
🔗 https://crm.smartremont.kz/deal/{lead['id']}
"""
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text)


async def send_daily_report(accepted_leads: list, missed_leads: list):
    text = f"""📊 Отчёт за {datetime.now().date().strftime('%d.%m.%Y')}:

✅ Принято: {len(accepted_leads)} шт.
❌ Упущено: {len(missed_leads)} шт.
"""
    if accepted_leads:
        text += "\n✅ Принятые:\n" + "\n".join(
            [f"• №{lead['id']} – {lead.get('name', '')}" for lead in accepted_leads]
        )

    if missed_leads:
        text += "\n\n❌ Упущенные:\n" + "\n".join(
            [f"• №{lead['id']} – {lead.get('name', '')}" for lead in missed_leads]
        )

    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text)


@dp.message(F.text == "/status")
async def handle_status(msg: Message):
    uptime = datetime.now() - start_time
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes = remainder // 60
    await msg.answer(
        f"🤖 Бот активен с {start_time.strftime('%H:%M:%S')} ⏱️ Аптайм: {hours} ч {minutes} мин."
    )


def start_bot():
    scheduler.start()
    print("✅ Бот запущен.")


def stop_bot():
    scheduler.shutdown()
    print("⛔ Бот остановлен.")
