import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent

load_dotenv(BASE_DIR / ".env")

BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
ADMIN_IDS_RAW: str = os.getenv("ADMIN_IDS", "")
ADMIN_IDS: list[int] = [
    int(x.strip()) for x in ADMIN_IDS_RAW.split(",") if x.strip().isdigit()
]

DB_PATH = BASE_DIR / "bot.db"
LOGO_PATH = BASE_DIR / "assets" / "logo.png"

# === РАЗДЕЛЫ (кнопки снизу) ===
# Ключ слева (kazan, sevastopol, perm, cp) - НЕ МЕНЯЙ, это callback_data.
# Текст справа - это то, что видит пользователь. Меняй свободно.
# Путь к файлу: telegram-bot/config.py
# Подробнее: telegram-bot/README_TUTORIAL.md
CATEGORIES: dict[str, str] = {
    "kazan": "КАЗНИ",
    "sevastopol": "СУИЦИДЫ",
    "perm": "ПХ\СЛИВЫ",
    "cp": "ЦП",
}

GREETING_TEXT = (
    "доброго дня, путник. \n\n"
    "выбирай. Или уходи."
)
