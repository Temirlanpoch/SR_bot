import os
import aiohttp
from bs4 import BeautifulSoup
from tele_utils import notify_new_lead

CRM_LOGIN = os.getenv("CRM_LOGIN")
CRM_PASS = os.getenv("CRM_PASS")
CRM_URL = os.getenv("CRM_URL", "https://crm.smartremont.kz")

session = None
accepted_ids = set()

async def login():
    global session
    session = aiohttp.ClientSession()
    payload = {
        "login": CRM_LOGIN,
        "password": CRM_PASS,
        "is_mobile": False,
        "os": "Windows",
        "user_agent": "Chrome"
    }
    async with session.post(f"{CRM_URL}/api/login", json=payload) as resp:
        return await resp.json()

async def fetch_leads():
    async with session.get(f"{CRM_URL}/leads") as resp:
        html = await resp.text()
        soup = BeautifulSoup(html, "html.parser")
        blocks = soup.select(".deal-card")
        leads = []
        for block in blocks:
            if "В работе" in block.text:
                deal_id = block.get("data-id")
                if deal_id not in accepted_ids:
                    name = block.select_one(".client-name").text.strip()
                    object_info = block.select_one(".object-info").text.strip()
                    date = block.select_one(".date").text.strip()
                    source = block.select_one(".source").text.strip()
                    link = f"{CRM_URL}/deal/{deal_id}"
                    leads.append({
                        "id": deal_id,
                        "name": name,
                        "object": object_info,
                        "date": date,
                        "source": source,
                        "link": link
                    })
        return leads

async def check_and_handle_leads():
    if session is None:
        await login()
    leads = await fetch_leads()
    for lead in leads:
        await notify_new_lead(lead)
        accepted_ids.add(lead["id"])