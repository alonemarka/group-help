from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def log_action(context, chat_id, action, user, reason=""):
    if context.bot_data.get("log_channel"):
        text = f"**Log:** {action}\n**Kullanıcı:** {user.mention_html()}\n**Grup:** {chat_id}\n**Sebep:** {reason}"
        context.bot.send_message(chat_id=context.bot_data["log_channel"], text=text, parse_mode='HTML')
