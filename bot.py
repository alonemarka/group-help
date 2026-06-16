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
        "Komutları öğrenmek için → /help",
        parse_mode='Markdown'
    )

async def help_command(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("📋 Genel Komutlar", callback_data="help_general")],
        [InlineKeyboardButton("🛠️ Admin Komutları", callback_data="help_admin")],
        [InlineKeyboardButton("🤖 AI Yardım", callback_data="help_ai")],
        [InlineKeyboardButton("⚙️ Moderasyon", callback_data="help_mod")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = (
        "🤖 **Group Help Bot - Komut Listesi**\n\n"
        "Aşağıdaki butonlardan istediğin kategoriyi seç.\n"
        "Tüm admin komutları **reply** ile kullanılır."
    )
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def button_callback(update: Update, context):
    query = update.callback_query
    await query.answer()

    if query.data == "help_general":
        text = (
            "📋 **Genel Komutlar**\n\n"
            "• `/start` - Botu başlat\n"
            "• `/help` - Bu menüyü göster\n"
            "• `/rules` - Grup kurallarını göster\n"
            "• `/info` - Kullanıcı bilgisi (kendin veya reply)\n"
            "• `/ai <soru>` - AI ile akıllı cevap al"
        )
elif query.data == "help_admin":
        text = (
            "🛠️ **Admin Komutları** (Reply ile kullan)\n\n"
            "• `/warn` - Uyarı ver\n"
            "• `/mute` - Sustur\n"
            "• `/unmute` - Susturmayı kaldır\n"
            "• `/kick` - At\n"
            "• `/ban` - Banla\n"
            "• `/purge` - Mesajları temizle\n"
            "• `/promote` veya `/admin` - Admin yap (reply, @user veya ID ile)\n"
            "• `/demote` veya `/unadmin` - Adminliği kaldır (reply, @user veya ID ile)"
        )
    elif query.data == "help_ai":
        text = (
            "🤖 **AI Yardım**\n\n"
            "`/ai merhaba nasılsın?`\n"
            "`/ai Python öğrenmek istiyorum`\n\n"
            "ai ile hızlı ve akıllı cevaplar alır."
        )
    elif query.data == "help_mod":
        text = (
            "⚙️ **Otomatik Moderasyon**\n\n"
            "• Anti-Flood (çok hızlı mesaj)\n"
            "• Log Kanalı (tüm işlemler loglanır)\n"
            "• Admin + Owner kontrolü"
        )
    
    await query.edit_message_text(text, parse_mode='Markdown')

def main():
    app = Application.builder().token(TOKEN).build()

    # Genel Komutlar
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    
    # User Komutları
    app.add_handler(CommandHandler("rules", user_h.rules))
    app.add_handler(CommandHandler("info", user_h.user_info))
    
    # Admin Komutları
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
    
    # Butonlar
    app.add_handler(CallbackQueryHandler(button_callback))

    print("🤖 Aşırı Gelişmiş Group Help Bot Başladı!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
