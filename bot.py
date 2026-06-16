import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler

from config import TOKEN, LOG_CHANNEL, OWNER_IDS
import handlers.admin as admin_h
import handlers.user as user_h
import handlers.moderation as mod
import handlers.ai_help as ai_h

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context):
    await update.message.reply_text(
        "✅ **Group Help Bot Başarıyla Aktif!**\n\n"
        "Gruba yönetici olarak ekleyin ve keyfini çıkarın.\n\n"
        "Tüm komutlar için → /help",
        parse_mode='Markdown'
    )

async def help_command(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("📋 Genel Komutlar", callback_data="help_commands")],
        [InlineKeyboardButton("🛠️ Admin Komutları", callback_data="help_admin")],
        [InlineKeyboardButton("🤖 AI Yardım", callback_data="help_ai")],
        [InlineKeyboardButton("⚙️ Moderasyon", callback_data="help_mod")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = "🤖 **Group Help Bot - Yardım Menüsü**\n\nAşağıdan kategori seç:"
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')

def main():
    app = Application.builder().token(TOKEN).build()

    # Genel Komutlar
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    
    # User Komutları
    app.add_handler(CommandHandler("rules", user_h.rules))
    app.add_handler(CommandHandler("info", user_h.user_info))
    
    # Admin Komutları
    app.add_handler(CommandHandler(["promote", "admin"], admin_h.promote))
    app.add_handler(CommandHandler(["demote", "unadmin"], admin_h.demote))
    app.add_handler(CommandHandler("warn", admin_h.warn))
    app.add_handler(CommandHandler("mute", admin_h.mute))
    app.add_handler(CommandHandler("unmute", admin_h.unmute))
    app.add_handler(CommandHandler("kick", admin_h.kick))
    app.add_handler(CommandHandler("ban", admin_h.ban))
    app.add_handler(CommandHandler("purge", admin_h.purge))
    
    # Moderasyon
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mod.moderation_handler))
    
    # AI
    app.add_handler(CommandHandler("ai", ai_h.ai_help))
    
    # Buton Callback
    app.add_handler(CallbackQueryHandler(user_h.button_callback))

    print("🤖 Aşırı Gelişmiş Group Help Bot Başladı!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
