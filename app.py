import os
import gc
from flask import Flask
import threading
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

app = Flask(__name__)

@app.route('/')
def home():
    return "🚗 Автосервис Бот работает"

@app.route('/health')
def health():
    return "OK", 200

# Упрощённые обработчики
async def start(update: Update, context: CallbackContext):
    keyboard = [["📋 МЕНЮ"], ["📱 СОЦСЕТИ"], ["📞 КОНТАКТЫ"], ["📍 АДРЕС"]]
    await update.message.reply_text("🚗 Добро пожаловать!\n👇 Выберите:", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
    gc.collect()

async def menu(update: Update, context: CallbackContext):
    await update.message.reply_text("🔧 УСЛУГИ:\n• Диагностика - 2000р\n• Чип-тюнинг - 5000р")
    gc.collect()

async def social(update: Update, context: CallbackContext):
    await update.message.reply_text("📱 СОЦСЕТИ:\n• Авито: avito.ru/...")
    gc.collect()

async def contacts(update: Update, context: CallbackContext):
    await update.message.reply_text("📞 КОНТАКТЫ:\n+7 922 433-35-45")
    gc.collect()

async def address(update: Update, context: CallbackContext):
    await update.message.reply_text("📍 АДРЕС:\nул. Пушкина, 9а\n🕒 9:00-19:00")
    gc.collect()

async def handle_message(update: Update, context: CallbackContext):
    text = update.message.text
    if text == "📋 МЕНЮ": await menu(update, context)
    elif text == "📱 СОЦСЕТИ": await social(update, context)
    elif text == "📞 КОНТАКТЫ": await contacts(update, context)
    elif text == "📍 АДРЕС": await address(update, context)
    gc.collect()

def run_bot():
    TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    if not TOKEN:
        print("❌ Нет токена")
        return
    
    app_bot = Application.builder().token(TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app_bot.run_polling()

threading.Thread(target=run_bot, daemon=True).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False, threaded=True, processes=1)
