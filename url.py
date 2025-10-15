import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import asyncio

TOKEN = ""

# Память для chat_id
users = set()

def get_ngrok_url():
    try:
        response = requests.get("http://127.0.0.1:4040/api/tunnels")
        return response.json()['tunnels'][0]['public_url']
    except:
        return "⚠️ Ngrok ещё не запущен"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    users.add(chat_id)  # сохраняем пользователя в память
    url = get_ngrok_url()
    await update.message.reply_text(f"🌐 Сайт запущен: {url}")

# Рассылка всем, кто писал боту
async def send_to_all(context: ContextTypes.DEFAULT_TYPE):
    url = get_ngrok_url()
    for chat_id in users:
        await context.bot.send_message(chat_id=chat_id, text=f"🌐 Сайт запущен: {url}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Любые текстовые сообщения
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    # Пример: через 5 секунд после старта рассылаем всем
    async def start_sending():
        await asyncio.sleep(5)
        await send_to_all(app)

    asyncio.run(asyncio.gather(
        app.run_polling(),
        start_sending()
    ))

