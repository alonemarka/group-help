from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import get_rules

async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rules_text = get_rules(update.effective_chat.id)
    await update.message.reply_text(f"📜 **Grup Kuralları:**\n\n{rules_text}", parse_mode='Markdown')

async def user_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user if not update.message.reply_to_message else update.message.reply_to_message.from_user
    text = f"👤 **Kullanıcı Bilgisi**\n\nID: `{user.id}`\nİsim: {user.full_name}"
    await update.message.reply_text(text, parse_mode='Markdown')

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "help_commands":
        text = "📋 Genel Komutlar:\n/rules - Kuralları göster\n/info - Kullanıcı bilgisi\n/ai <soru> - AI ile sor"
    elif query.data == "help_admin":
        text = "🛠️ Admin Komutları:\n/warn, /mute, /unmute, /kick, /ban, /purge"
    elif query.data == "help_ai":
        text = "🤖 /ai komutu ile Groq AI ile konuşabilirsiniz."
    
    await query.edit_message_text(text)
