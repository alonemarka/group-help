import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", 0))
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Birden fazla OWNER_ID desteği
OWNER_IDS = os.getenv("OWNER_ID", "0")
# Virgülle ayrılmışsa listeye çevir
if isinstance(OWNER_IDS, str):
    OWNER_IDS = [int(x.strip()) for x in OWNER_IDS.split(",") if x.strip().isdigit()]
else:
    OWNER_IDS = [int(OWNER_IDS)]

# Moderasyon Ayarları
ANTI_FLOOD = True
FLOOD_LIMIT = 6
FLOOD_TIME = 8

WELCOME_ENABLED = True
GOODBYE_ENABLED = True
