import os, asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
TOKEN = os.getenv("BOT_TOKEN")
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔒 BOT PRIVATO 3.0 ONLINE\n\n/segreto - rispondi a foto/video -> si autodistrugge in 15s\n/blur - rispondi a foto -> foto sfocata\n/anonimo testo - manda anonimo\n/pulisci - cancella 100 messaggi\n/panico - cancella tutto")
async def segreto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message: return
    replied = update.message.reply_to_message
    chat_id = update.effective_chat.id
    if replied.photo:
        sent = await context.bot.send_photo(chat_id, replied.photo[-1].file_id, caption="🔒 15s")
    elif replied.video:
        sent = await context.bot.send_video(chat_id, replied.video.file_id, caption="🔒 15s")
    else: return
    await asyncio.sleep(15)
    for mid in [replied.message_id, update.message.message_id, sent.message_id]:
        try: await context.bot.delete_message(chat_id, mid)
        except: pass
async def blur(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message or not update.message.reply_to_message.photo: return
    await context.bot.send_photo(update.effective_chat.id, update.message.reply_to_message.photo[-1].file_id, has_spoiler=True)
    try:
        await context.bot.delete_message(update.effective_chat.id, update.message.reply_to_message.message_id)
        await context.bot.delete_message(update.effective_chat.id, update.message.message_id)
    except: pass
async def anonimo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return
    testo = " ".join(context.args)
    try: await context.bot.delete_message(update.effective_chat.id, update.message.message_id)
    except: pass
    await context.bot.send_message(update.effective_chat.id, f"👻 ANONIMO:\n{testo}")
async def pulisci(update: Update, context: ContextTypes.DEFAULT_TYPE):
    base = update.message.message_id
    for i in range(1, 101):
        try: await context.bot.delete_message(update.effective_chat.id, base - i)
        except: pass
async def panico(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for i in range(1, 300):
        try: await context.bot.delete_message(update.effective_chat.id, update.message.message_id - i)
        except: pass
app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("segreto", segreto))
app.add_handler(CommandHandler("blur", blur))
app.add_handler(CommandHandler("anonimo", anonimo))
app.add_handler(CommandHandler("pulisci", pulisci))
app.add_handler(CommandHandler("panico", panico))
print("BOT ONLINE")
app.run_polling()
