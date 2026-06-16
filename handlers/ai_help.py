from telegram import Update
from telegram.ext import ContextTypes
from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

async def ai_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❓ Lütfen bir soru sorun.\nÖrnek: `/ai Bugün hava nasıl?`")
        return
    
    query = " ".join(context.args)
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": query}],
            model="llama-3.1-8b-instant",   # Güncel ve hızlı model
            temperature=0.7,
            max_tokens=700,
        )
        answer = chat_completion.choices[0].message.content
        await update.message.reply_text(answer[:4000], parse_mode='Markdown')
    except Exception as e:
        await update.message.reply_text(f"❌ AI hatası: {str(e)[:400]}")
