import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", 0))
LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", 0))
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Moderasyon Ayarları
ANTI_FLOOD = True
FLOOD_LIMIT = 6
FLOOD_TIME = 8

# Diğer ayarlar
WELCOME_ENABLED = True
GOODBYE_ENABLED = True
