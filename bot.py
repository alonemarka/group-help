import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from config import TOKEN, LOG_CHANNEL, OWNER_ID
import handlers.admin as admin_h
import handlers.user as user_h
import handlers.moderation as mod
import handlers.ai_help as ai_h

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context):
    await update.message.reply_text(
        "✅ **Group Help Bot Başarıyla Aktif!**\n\n"
        "Gruba yönetici olarak ekleyin ve keyfini çıkarın.",
        parse_mode='Markdown'
    )

async def help_command(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("📋 Genel Komutlar", callback_data="help_commands")],
        [InlineKeyboardButton("🛠️ Admin Komutları", callback_data="help_admin")],
        [InlineKeyboardButton("🤖 AI Yardım", callback_data="help_ai")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("**Group Help Bot Menüsü**", reply_markup=reply_markup, parse_mode='Markdown')

def main():
    app = Application.builder().token(TOKEN).build()

    # Genel
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    
    # User
    app.add_handler(CommandHandler("rules", user_h.rules))
    app.add_handler(CommandHandler("info", user_h.user_info))
    
    # Admin
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
    
    # Callback
    app.add_handler(CallbackQueryHandler(user_h.button_callback))

    print("🤖 Aşırı Gelişmiş Group Help Bot Başladı!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
