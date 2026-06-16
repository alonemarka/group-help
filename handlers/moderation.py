from telegram import Update
from telegram.ext import ContextTypes
import time
from config import ANTI_FLOOD, FLOOD_LIMIT, FLOOD_TIME
from database import add_warning

async def moderation_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    
    user = update.message.from_user
    chat_id = update.effective_chat.id
    current_time = time.time()

    # Flood Kontrolü
    if ANTI_FLOOD:
        if 'flood' not in context.bot_data:
            context.bot_data['flood'] = {}
        key = f"{chat_id}_{user.id}"
        if key not in context.bot_data['flood']:
            context.bot_data['flood'][key] = {'time': current_time, 'count': 1}
        else:
            data = context.bot_data['flood'][key]
            if current_time - data['time'] < FLOOD_TIME:
                data['count'] += 1
                if data['count'] >= FLOOD_LIMIT:
                    await update.message.reply_text(f"🚫 {user.mention_html()} flood yaptığı için uyarıldı!", parse_mode='HTML')
                    await add_warning(user.id, chat_id)
                    del context.bot_data['flood'][key]
                    return
            else:
                data['time'] = current_time
                data['count'] = 1
