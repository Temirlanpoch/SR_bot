import re
from bs4 import BeautifulSoup

def extract_name(full_name: str) -> str:
    """Извлекает только имя из полного ФИО (например, 'Исаев Темирлан Арманович' -> 'Темирлан')."""
    parts = full_name.strip().split()
    if len(parts) >= 2:
        return parts[1]
    return parts[0] if parts else ""

def close_popups_and_accept(html: str) -> bool:
    """
    Проверяет HTML и определяет, были ли найдены всплывающие окна и возможность принять лид.
    Возвращает True, если окно успешно "обработано", иначе False.
    (Эта функция используется как логический фильтр, реальное закрытие делает JS.)
    """
    soup = BeautifulSoup(html, 'html.parser')
    popup = soup.find("div", {"class": "popup"})
    return popup is not None
