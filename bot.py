import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from config import TOKEN, LOG_CHANNEL, OWNER_ID
import handlers.admin as admin
import handlers.user as user
import handlers.moderation as mod
import handlers.ai_help as ai

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context):
    await update.message.reply_text(
        "✅ **Group Help Bot Aktif!**\n\n"
        "Gruba ekle ve /help yaz.",
        parse_mode='Markdown'
    )

async def help_command(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("📋 Komutlar", callback_data="help_commands")],
        [InlineKeyboardButton("🛠️ Admin Komutları", callback_data="help_admin")],
        [InlineKeyboardButton("🤖 AI Yardım", callback_data="help_ai")]
    ]
    await update.message.reply_text("**Group Help Bot Menü**", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

def main():
    app = Application.builder().token(TOKEN).build()

    # Komutlar
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("rules", user.rules))
    app.add_handler(CommandHandler("info", user.user_info))

    # Admin komutları
    app.add_handler(CommandHandler("warn", admin.warn))
    app.add_handler(CommandHandler("mute", admin.mute))
    app.add_handler(CommandHandler("unmute", admin.unmute))
    app.add_handler(CommandHandler("kick", admin.kick))
    app.add_handler(CommandHandler("ban", admin.ban))
    app.add_handler(CommandHandler("purge", admin.purge))

    # Moderasyon
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mod.moderation_handler))

    # AI Yardım
    app.add_handler(CommandHandler("ai", ai.ai_help))

    # Callback
    app.add_handler(CallbackQueryHandler(user.button_callback))

    print("🤖 Bot Başladı!")
    app.run_polling()

if __name__ == '__main__':
    main()
