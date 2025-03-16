import google.generativeai as genai
from telegram.constants import ChatAction
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 🔑 API kalitlari
GOOGLE_API_KEY = "AIzaSyC8vhytL9sAZ4O0JU70V0KVS0HJPIFYQt8"
TELEGRAM_BOT_TOKEN = "7555872198:AAF5_CSWu8_d-AIPYtXURwxB0AJ4REglAAs"

# 🌟 Google Gemini AI API-ni sozlash
genai.configure(api_key=GOOGLE_API_KEY)

# 🧠 Foydalanuvchi xabarlar tarixini saqlash
user_history = {}


# 🏁 /start buyrug'iga javob berish
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    user_history[user_id] = []  # Foydalanuvchi tarixini boshlash

    await update.message.reply_text(
        "👋 Salom! Men Google Gemini AI asosida ishlovchi Telegram botman.\nMenga istalgan savolni bering! 🚀"
    )


# 💬 Foydalanuvchi xabarlarini qayta ishlash
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    user_message = update.message.text  # Foydalanuvchi xabari

    # ⏳ "Typing..." effekti va kutish xabari
    await update.message.chat.send_action(ChatAction.TYPING)
    message = await update.message.reply_text("🕰 Обрабатывает сообщение...")

    # 🔄 Foydalanuvchi tarixini yangilash (faqat oxirgi 5 ta xabarni saqlash)
    if user_id not in user_history:
        user_history[user_id] = []

    user_history[user_id].append(user_message)
    user_history[user_id] = user_history[user_id][-5:]

    try:
        # ✅ Gemini AI modeli orqali javob olish
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        response = model.generate_content(
            [user_message],  # List shaklida yuborish muhim!
            generation_config={"temperature": 0.7, "max_output_tokens": 100}
        )
        bot_reply = response.text

        # 🔄 Kutish xabarini o‘chirish va javobni jo‘natish
        await message.delete()
        await update.message.reply_text(bot_reply)

    except Exception as e:
        await message.delete()
        await update.message.reply_text(f"❌ Xatolik yuz berdi. Keyinroq urinib ko‘ring.\n\n🔍 Xato tafsiloti: {str(e)}")
        print(f"Xato tafsiloti: {e}")


# ❌ Xatolarni qayd qilish
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Xatolik: {context.error}")


# 🚀 Asosiy bot funksiyasi
def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # 🔹 /start komandasi
    application.add_handler(CommandHandler("start", start))

    # 🔹 Oddiy xabarlar
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # 🔹 Xatolarni qayd qilish
    application.add_error_handler(error)

    print("🤖 Bot ishga tushdi...")
    application.run_polling()


# 🔥 Botni ishga tushirish
if __name__ == "__main__":
    main()
