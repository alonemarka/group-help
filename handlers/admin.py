from telegram import Update, ChatAdministratorRights
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
        return member.status in ["administrator", "creator"]
    except:
        return False

# ====================== YENİ KOMUTLAR ======================

async def promote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin_or_owner(update):
        await update.message.reply_text("⛔ Bu komutu kullanmak için **admin** olman lazım!")
        return

    user = None
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
    elif context.args:
        arg = context.args[0]
        if arg.startswith('@'):
            try:
                user = await context.bot.get_chat(arg)
            except:
                await update.message.reply_text("❌ Kullanıcı bulunamadı.")
                return
        else:
            try:
                user_id = int(arg)
                user = await context.bot.get_chat(user_id)
            except:
                await update.message.reply_text("❌ Geçerli ID veya @kullanıcı girin.")
                return

    if not user:
        await update.message.reply_text("⚠️ Bir mesaja reply yap veya `/promote @kullanıcı` ya da `/promote ID` yaz.")
        return

    try:
        rights = ChatAdministratorRights(
            can_manage_chat=True,
            can_delete_messages=True,
            can_manage_video_chats=True,
            can_restrict_members=True,
            can_promote_members=False,   # Güvenlik için
            can_change_info=True,
            can_invite_users=True,
            can_post_messages=True,
            can_edit_messages=True,
            can_pin_messages=True
        )
        await context.bot.promote_chat_member(update.effective_chat.id, user.id, rights)
        await update.message.reply_text(f"✅ {user.mention_html()} **admin** yapıldı!", parse_mode='HTML')
        await log_action(context, update.effective_chat.id, "PROMOTE", user)
    except Exception as e:
        await update.message.reply_text(f"❌ Admin yapma hatası: {str(e)[:200]}")

async def demote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin_or_owner(update):
        await update.message.reply_text("⛔ Bu komutu kullanmak için **admin** olman lazım!")
        return

    user = None
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
    elif context.args:
        arg = context.args[0]
        if arg.startswith('@'):
            try:
                user = await context.bot.get_chat(arg)
            except:
                await update.message.reply_text("❌ Kullanıcı bulunamadı.")
                return
        else:
            try:
                user_id = int(arg)
                user = await context.bot.get_chat(user_id)
            except:
                await update.message.reply_text("❌ Geçerli ID veya @kullanıcı girin.")
                return

    if not user:
        await update.message.reply_text("⚠️ Bir mesaja reply yap veya `/demote @kullanıcı` ya da `/demote ID` yaz.")
        return

    try:
        await context.bot.promote_chat_member(update.effective_chat.id, user.id, can_manage_chat=False)
        await update.message.reply_text(f"✅ {user.mention_html()} adminlikten alındı.", parse_mode='HTML')
        await log_action(context, update.effective_chat.id, "DEMOTE", user)
    except Exception as e:
        await update.message.reply_text(f"❌ Demote hatası: {str(e)[:200]}")

# ====================== ESKİ KOMUTLAR (Kısaca) ======================

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

# Diğer komutlar (mute, unmute, kick, ban, purge) aynı kalıyor...
# (Önceki mesajımdan kopyala-yapıştır yap, yer kaplamasın)

async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin_or_owner(update): 
        await update.message.reply_text("⛔ Bu komutu kullanmak için **admin** olman lazım!"); return
    if not update.message.reply_to_message: return
    user = update.message.reply_to_message.from_user
    await context.bot.restrict_chat_member(update.effective_chat.id, user.id, can_send_messages=False)
    await update.message.reply_text(f"🔇 {user.mention_html()} susturuldu.", parse_mode='HTML')

async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin_or_owner(update): 
        await update.message.reply_text("⛔ Bu komutu kullanmak için **admin** olman lazım!"); return
    if not update.message.reply_to_message: return
    user = update.message.reply_to_message.from_user
    await context.bot.restrict_chat_member(update.effective_chat.id, user.id, can_send_messages=True)
    await update.message.reply_text(f"🔊 {user.mention_html()} susturulması kaldırıldı.", parse_mode='HTML')

async def kick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin_or_owner(update): 
        await update.message.reply_text("⛔ Bu komutu kullanmak için **admin** olman lazım!"); return
    if not update.message.reply_to_message: return
    user = update.message.reply_to_message.from_user
    await context.bot.ban_chat_member(update.effective_chat.id, user.id)
    await context.bot.unban_chat_member(update.effective_chat.id, user.id)
    await update.message.reply_text(f"👢 {user.mention_html()} gruptan atıldı.", parse_mode='HTML')

async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin_or_owner(update): 
        await update.message.reply_text("⛔ Bu komutu kullanmak için **admin** olman lazım!"); return
    if not update.message.reply_to_message: return
    user = update.message.reply_to_message.from_user
    await context.bot.ban_chat_member(update.effective_chat.id, user.id)
    await update.message.reply_text(f"⛔ {user.mention_html()} banlandı.", parse_mode='HTML')

async def purge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin_or_owner(update): 
        await update.message.reply_text("⛔ Bu komutu kullanmak için **admin** olman lazım!"); return
    if not update.message.reply_to_message: return
    try:
        await context.bot.delete_messages(update.effective_chat.id, list(range(update.message.reply_to_message.message_id, update.message.message_id + 1)))
        await update.message.reply_text("🧹 Mesajlar temizlendi.")
    except:
        await update.message.reply_text("Purge hatası oluştu.")
