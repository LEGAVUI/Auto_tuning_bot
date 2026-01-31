import os
import asyncio
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

# Обработчики
async def start(update: Update, context: CallbackContext):
    keyboard = [["📋 МЕНЮ"], ["📱 СОЦСЕТИ"], ["📞 КОНТАКТЫ"], ["📍 АДРЕС"]]
    await update.message.reply_text(
        "🚗 Добро пожаловать в автосервис!\n👇 Выберите раздел:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

async def menu(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "🔧 НАШИ УСЛУГИ:\n\n"
        "• Диагностика - 2000р\n"
        "• Чип-тюнинг - 5000р\n"
        "• Прошивка ЭБУ - 4500р\n"
        "• Услуги автоэлектрика"
    )

async def social(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "📱 МЫ В СОЦСЕТЯХ:\n\n"
        "• Instagram: instagram.com/chiptuning_service_fake\n\n"
        "• Авито: avito.ru/avtoelektrik_diagnost_7856909160"
    )

async def contacts(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "📞 НАШИ КОНТАКТЫ:\n\n"
        "• Телефон: +7 922 433-35-45\n"
        "• WhatsApp: wa.me/79224333545\n"
        "• Telegram: t.me/+79224333545"
    )

async def address(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "📍 НАШ АДРЕС:\nул. Пушкина, Дом 9а\n\n🕒 9:00-19:00 ежедневно"
    )

async def handle_message(update: Update, context: CallbackContext):
    text = update.message.text
    
    if text == "📋 МЕНЮ":
        await menu(update, context)
    elif text == "📱 СОЦСЕТИ":
        await social(update, context)
    elif text == "📞 КОНТАКТЫ":
        await contacts(update, context)
    elif text == "📍 АДРЕС":
        await address(update, context)

# Запуск бота с правильным event loop
def run_bot():
    TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    
    if not TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN не найден")
        # Ждём токен
        import time
        for _ in range(30):
            TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
            if TOKEN:
                break
            time.sleep(2)
        
        if not TOKEN:
            print("❌ Токен так и не найден")
            return
    
    print("✅ Токен найден! Запускаю бота...")
    
    # Создаём новый event loop для этого потока
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # Создаём приложение
    application = Application.builder().token(TOKEN).build()
    
    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🤖 Бот запущен и слушает сообщения...")
    
    # Запускаем бота в этом event loop
    try:
        loop.run_until_complete(application.run_polling())
    finally:
        loop.close()

# Запускаем бота в отдельном потоке
bot_thread = threading.Thread(target=run_bot, daemon=True)
bot_thread.start()

if __name__ == '__main__':
    print("🌐 Запуск Flask сервера...")
    print("=" * 50)
    print("🚗 АВТОСЕРВИС БОТ ЗАПУЩЕН")
    print("=" * 50)
    app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)
