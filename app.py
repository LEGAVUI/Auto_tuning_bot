import os
import time
from flask import Flask
import threading
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

print("=" * 50)
print("🚗 АВТОСЕРВИС БОТ НА KOYEB (PRO VERSION)")
print("=" * 50)

app = Flask(__name__)

@app.route('/')
def home():
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>🚗 Автосервис Бот</title>
        <style>
            body {{ font-family: Arial, sans-serif; text-align: center; padding: 50px; background: #f5f5f5; }}
            .container {{ background: white; padding: 40px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); max-width: 600px; margin: 0 auto; }}
            h1 {{ color: #2c3e50; }}
            .status {{ color: #27ae60; font-size: 1.2em; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚗 Автосервис Бот</h1>
            <div class="status">✅ Бот работает на Koyeb</div>
            <p>🤖 Версия: Python-Telegram-Bot 20.7</p>
            <p>⚡ Отвечает мгновенно</p>
            <p>🕒 Время сервера: {current_time}</p>
        </div>
    </body>
    </html>
    """

@app.route('/health')
def health():
    return "OK", 200

# Telegram бот
async def start(update: Update, context: CallbackContext):
    keyboard = [
        ["📋 МЕНЮ"],
        ["📱 СОЦСЕТИ", "📞 КОНТАКТЫ"],
        ["📍 АДРЕС"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "🚗 Добро пожаловать в автосервис!\n👇 Выберите раздел:",
        reply_markup=reply_markup
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
    avito_link = "https://www.avito.ru/kizilyurt/predlozheniya_uslug/avtoelektrik_diagnost_7856909160"
    await update.message.reply_text(
        "📱 МЫ В СОЦСЕТЯХ:\n\n"
        "• Instagram: instagram.com/chiptuning_service_fake\n\n"
        f"• <a href='{avito_link}'>Авито</a> - наши услуги автоэлектрика\n\n"
        "Нажмите на 'Авито' для перехода",
        parse_mode='HTML'
    )

async def contacts(update: Update, context: CallbackContext):
    phone = "+7 922 433-35-45"
    whatsapp = "https://wa.me/79224333545"
    telegram = "https://t.me/+79224333545"
    
    await update.message.reply_text(
        "📞 НАШИ КОНТАКТЫ:\n\n"
        f"• Телефон: {phone}\n\n"
        f"• <a href='{whatsapp}'>WhatsApp</a>\n"
        f"• <a href='{telegram}'>Telegram</a>\n\n"
        "Нажмите на ссылки для связи",
        parse_mode='HTML'
    )

async def address(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "📍 НАШ АДРЕС:\n"
        "ул. Пушкина, Дом 9а\n\n"
        "🕒 9:00-19:00 ежедневно"
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
    else:
        await update.message.reply_text("Выберите вариант из меню ниже 👇")

def run_telegram_bot():
    TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    
    if not TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN не найден")
        print("⏳ Ожидание токена...")
        for i in range(30):
            TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
            if TOKEN:
                break
            time.sleep(2)
        
        if not TOKEN:
            print("❌ Токен так и не найден. Бот не запущен.")
            return
    
    print("✅ Токен найден! Запускаю бота...")
    
    # Создаём приложение
    application = Application.builder().token(TOKEN).build()
    
    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🤖 Бот запущен и слушает сообщения...")
    
    # Запускаем бота
    application.run_polling(allowed_updates=Update.ALL_TYPES)

# Запускаем бота в отдельном потоке
threading.Thread(target=run_telegram_bot, daemon=True).start()

if __name__ == '__main__':
    print("🌐 Запуск Flask сервера...")
    app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)
