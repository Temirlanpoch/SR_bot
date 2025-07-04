# lead_handler.py

import os
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from datetime import datetime
from tele_utils import notify_new_lead, notify_missed_lead, notify_error
from utils import extract_name, close_popups_and_accept

CRM_LOGIN = os.getenv("CRM_LOGIN")
CRM_PASSWORD = os.getenv("CRM_PASSWORD")
CRM_BASE_URL = "https://crm.smartremont.kz"

session_cookies = None


async def login():
    global session_cookies
    async with aiohttp.ClientSession() as session:
        payload = {
            "login": CRM_LOGIN,
            "password": CRM_PASSWORD
        }

        async with session.post(f"{CRM_BASE_URL}/api/login", json=payload) as resp:
            content_type = resp.headers.get('Content-Type', '')
            if 'application/json' not in content_type:
                text = await resp.text()
                print("⚠️ Ожидался JSON, но получен HTML. Возможная ошибка авторизации.")
                print(text[:1000])  # вывод первых 1000 символов HTML
                raise ValueError("Сервер вернул не JSON — возможно, ошибка авторизации или капча")

            data = await resp.json()
            session_cookies = session.cookie_jar.filter_cookies(CRM_BASE_URL)
            return data


async def fetch_leads():
    global session_cookies
    async with aiohttp.ClientSession(cookies=session_cookies) as session:
        async with session.get(f"{CRM_BASE_URL}/api/leads") as resp:
            return await resp.json()


async def check_and_handle_leads():
    try:
        await login()
        leads = await fetch_leads()

        for lead in leads.get("items", []):
            lead_id = lead["id"]
            status = lead.get("status", "").lower()
            assigned = lead.get("assigned_to_user")

            # Пропускаем, если лид уже в работе
            if status == "в работе" and assigned:
                continue

            accepted = await close_popups_and_accept(lead_id)

            if accepted:
                await notify_new_lead(lead)
            else:
                await notify_missed_lead(lead)

    except Exception as e:
        await notify_error(str(e))
        print(f"Ошибка в check_and_handle_leads: {e}")
