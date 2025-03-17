import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Telegram va Gemini API kalitlarini kiriting
TELEGRAM_BOT_TOKEN = "7555872198:AAF5_CSWu8_d-AIPYtXURwxB0AJ4REglAAs"
GEMINI_API_KEY = "AIzaSyC8vhytL9sAZ4O0JU70V0KVS0HJPIFYQt8"

# Gemini API sozlamalari
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Привет! Я бот, работающий с Gemini AI. Отправьте ваш вопрос!")

async def ask_gemini(update: Update, context: CallbackContext):
    user_message = update.message.text

    try:
        response = model.generate_content(user_message)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text("Xatolik yuz berdi: " + str(e))

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ask_gemini))

    print("Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
