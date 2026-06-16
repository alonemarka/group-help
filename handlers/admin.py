from telegram import Update
from telegram.ext import ContextTypes
from database import add_warning, reset_warnings
from utils.helpers import log_action
from config import OWNER_IDS

def is_owner(user_id: int) -> bool:
    return user_id in OWNER_IDS

async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id) and not update.effective_chat.get_member(update.effective_user.id).status in ["administrator", "creator"]:
        return
    if not update.message.reply_to_message: 
        await update.message.reply_text("Bir mesaja reply yaparak komut verin.")
        return
    
    user = update.message.reply_to_message.from_user
    chat_id = update.effective_chat.id
    count = add_warning(user.id, chat_id)
    
    await update.message.reply_text(f"⚠️ {user.mention_html()} uyarıldı! ({count}/3)", parse_mode='HTML')
    await log_action(context, chat_id, "WARN", user, " ".join(context.args) or "Belirtilmedi")

# Diğer fonksiyonlar için de aynı owner kontrolünü ekleyelim
async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id) and not update.effective_chat.get_member(update.effective_user.id).status in ["administrator", "creator"]:
        return
    if not update.message.reply_to_message: return
    user = update.message.reply_to_message.from_user
    await context.bot.restrict_chat_member(update.effective_chat.id, user.id, can_send_messages=False)
    await update.message.reply_text(f"🔇 {user.mention_html()} susturuldu.", parse_mode='HTML')

async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id) and not update.effective_chat.get_member(update.effective_user.id).status in ["administrator", "creator"]:
        return
    if not update.message.reply_to_message: return
    user = update.message.reply_to_message.from_user
    await context.bot.restrict_chat_member(update.effective_chat.id, user.id, can_send_messages=True)
    await update.message.reply_text(f"🔊 {user.mention_html()} susturulması kaldırıldı.", parse_mode='HTML')

async def kick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id) and not update.effective_chat.get_member(update.effective_user.id).status in ["administrator", "creator"]:
        return
    if not update.message.reply_to_message: return
    user = update.message.reply_to_message.from_user
    await context.bot.ban_chat_member(update.effective_chat.id, user.id)
    await context.bot.unban_chat_member(update.effective_chat.id, user.id)
    await update.message.reply_text(f"👢 {user.mention_html()} gruptan atıldı.", parse_mode='HTML')

async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id) and not update.effective_chat.get_member(update.effective_user.id).status in ["administrator", "creator"]:
        return
    if not update.message.reply_to_message: return
    user = update.message.reply_to_message.from_user
    await context.bot.ban_chat_member(update.effective_chat.id, user.id)
    await update.message.reply_text(f"⛔ {user.mention_html()} banlandı.", parse_mode='HTML')

async def purge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id) and not update.effective_chat.get_member(update.effective_user.id).status in ["administrator", "creator"]:
        return
    if not update.message.reply_to_message: return
    try:
        await context.bot.delete_messages(update.effective_chat.id, 
                                         list(range(update.message.reply_to_message.message_id, update.message.message_id + 1)))
        await update.message.reply_text("🧹 Mesajlar temizlendi.")
    except:
        await update.message.reply_text("Purge sırasında hata oluştu.")
