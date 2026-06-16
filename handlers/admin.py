from telegram import Update
from telegram.ext import ContextTypes
from database import add_warning
from utils.helpers import log_action
from config import OWNER_IDS

def is_admin_or_owner(update: Update) -> bool:
    user_id = update.effective_user.id
    chat = update.effective_chat
    
    if user_id in OWNER_IDS:
        return True
    
    try:
        member = chat.get_member(user_id)
        if member.status in ["administrator", "creator"]:
            return True
        else:
            return False
    except Exception as e:
        print(f"[DEBUG] Admin kontrol hatası: {e}")
        return False

async def check_bot_admin(chat):
    try:
        bot_member = await chat.get_member(chat.bot.id)  # Bot'un kendi yetkisini kontrol et
        return bot_member.status in ["administrator", "creator"]
    except:
        return False

# ====================== KOMUTLAR ======================

async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin_or_owner(update):
        await update.message.reply_text("⛔ Bu komutu kullanmak için **admin** olman lazım!")
        return
    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ Bir mesaja **reply** yaparak komut verin.")
        return

    user = update.message.reply_to_message.from_user
    count = add_warning(user.id, update.effective_chat.id)
    
    await update.message.reply_text(f"⚠️ {user.mention_html()} uyarıldı! ({count}/3)", parse_mode='HTML')
    await log_action(context, update.effective_chat.id, "WARN", user)

async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin_or_owner(update):
        await update.message.reply_text("⛔ Bu komutu kullanmak için **admin** olman lazım!")
        return
    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ Reply ile kullanın.")
        return

    user = update.message.reply_to_message.from_user
    await context.bot.restrict_chat_member(update.effective_chat.id, user.id, can_send_messages=False)
    await update.message.reply_text(f"🔇 {user.mention_html()} susturuldu.", parse_mode='HTML')

async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin_or_owner(update):
        await update.message.reply_text("⛔ Bu komutu kullanmak için **admin** olman lazım!")
        return
    if not update.message.reply_to_message: return

    user = update.message.reply_to_message.from_user
    await context.bot.restrict_chat_member(update.effective_chat.id, user.id, can_send_messages=True)
    await update.message.reply_text(f"🔊 {user.mention_html()} susturulması kaldırıldı.", parse_mode='HTML')

async def kick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin_or_owner(update):
        await update.message.reply_text("⛔ Bu komutu kullanmak için **admin** olman lazım!")
        return
    if not update.message.reply_to_message: return

    user = update.message.reply_to_message.from_user
    await context.bot.ban_chat_member(update.effective_chat.id, user.id)
    await context.bot.unban_chat_member(update.effective_chat.id, user.id)
    await update.message.reply_text(f"👢 {user.mention_html()} gruptan atıldı.", parse_mode='HTML')

async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin_or_owner(update):
        await update.message.reply_text("⛔ Bu komutu kullanmak için **admin** olman lazım!")
        return
    if not update.message.reply_to_message: return

    user = update.message.reply_to_message.from_user
    await context.bot.ban_chat_member(update.effective_chat.id, user.id)
    await update.message.reply_text(f"⛔ {user.mention_html()} banlandı.", parse_mode='HTML')

async def purge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin_or_owner(update):
        await update.message.reply_text("⛔ Bu komutu kullanmak için **admin** olman lazım!")
        return
    if not update.message.reply_to_message: 
        await update.message.reply_text("⚠️ Reply ile kullanın.")
        return

    try:
        await context.bot.delete_messages(
            update.effective_chat.id,
            list(range(update.message.reply_to_message.message_id, update.message.message_id + 1))
        )
        await update.message.reply_text("🧹 Mesajlar temizlendi.")
    except Exception as e:
        await update.message.reply_text(f"Purge hatası: {str(e)[:200]}")
