import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("8959507942:AAGyl_GNhVz1_6P1yO-0PpDun-txFUw8gvY")
LOG_CHANNEL = os.getenv("-1004426556227")  # -100xxxxxxxxxx
OWNER_ID = int(os.getenv("8973632679"))
GROQ_API_KEY = os.getenv("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")

# Filtre ayarları
ANTI_FLOOD = True
FLOOD_LIMIT = 5
FLOOD_TIME = 10
