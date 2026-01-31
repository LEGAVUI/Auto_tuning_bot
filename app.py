import os
import requests
import time
from flask import Flask
import threading
from datetime import datetime

print("=" * 50)
print("🚗 АВТОСЕРВИС БОТ НА KOYEB")
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
        <meta charset="utf-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 50px;
                background: #f5f5f5;
            }}
            .container {{
                background: white;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                max-width: 600px;
                margin: 0 auto;
            }}
            h1 {{
                color: #2c3e50;
            }}
            .status {{
                color: #27ae60;
                font-size: 1.2em;
                margin: 20px 0;
            }}
            .info {{
                text-align: left;
                margin: 20px 0;
                padding: 15px;
                background: #f8f9fa;
                border-radius: 5px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚗 Автосервис Бот</h1>
            <div class="status">✅ Бот работает на Koyeb</div>
            
            <div class="info">
                <p><strong>🤖 Функции бота:</strong></p>
                <ul>
                    <li>Меню услуг автосервиса</li>
                    <li>Ссылка на Авито с услугами автоэлектрика</li>
                    <li>Контакты для связи: +7 922 433-35-45</li>
                    <li>Адрес: ул. Пушкина, Дом 9а</li>
                </ul>
            </div>
            
            <p>Бот работает 24/7 без перерывов</p>
            <p>🕒 Время сервера: {current_time}</p>
        </div>
    </body>
    </html>
    """

@app.route('/health')
def health():
    return "OK", 200

# Telegram бот
def telegram_bot():
    TOKEN = os.environ.get('8248650023:AAHYIqTPxUFxVw_RdgqiGOHgyphcna1U8Mo')
    
    # Ожидание токена, если он не сразу доступен
    while not TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN не найден")
        print("💡 Добавьте токен в Koyeb: Settings → Environment Variables")
        print("⏳ Ожидание 10 секунд...")
        time.sleep(10)
        TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    
    print("✅ Токен найден! Запускаю бота...")
    
    API_URL = f"https://api.telegram.org/bot{TOKEN}/"
    
    # Контакты
    AVITO_LINK = "https://www.avito.ru/kizilyurt/predlozheniya_uslug/avtoelektrik_diagnost_7856909160"
    PHONE_NUMBER = "+7 922 433-35-45"
    WHATSAPP_LINK = "https://wa.me/79224333545"
    TELEGRAM_LINK = "https://t.me/+79224333545"
    
    # Меню
    keyboard = {
        "keyboard": [
            [{"text": "📋 МЕНЮ"}],
            [{"text": "📱 СОЦСЕТИ"}], 
            [{"text": "📞 КОНТАКТЫ"}],
            [{"text": "📍 АДРЕС"}]
        ],
        "resize_keyboard": True
    }
    
    last_update_id = 0
    
    print("✅ Telegram бот запущен")
    print("🤖 Ожидание сообщений...")
    
    while True:
        try:
            resp = requests.get(
                f"{API_URL}getUpdates",
                params={"offset": last_update_id + 1, "timeout": 10},
                timeout=15
            )
            
            if resp.status_code == 200:
                data = resp.json()
                if data.get("ok"):
                    updates = data.get("result", [])
                    
                    for update in updates:
                        last_update_id = update["update_id"]
                        
                        if "message" in update:
                            chat_id = update["message"]["chat"]["id"]
                            text = update["message"].get("text", "")
                            
                            # /start
                            if "/start" in text.lower():
                                requests.post(f"{API_URL}sendMessage", json={
                                    "chat_id": chat_id,
                                    "text": "🚗 Добро пожаловать в автосервис!\n👇 Выберите раздел:",
                                    "reply_markup": keyboard
                                })
                            
                            # Меню
                            elif text == "📋 МЕНЮ":
                                requests.post(f"{API_URL}sendMessage", json={
                                    "chat_id": chat_id,
                                    "text": "🔧 НАШИ УСЛУГИ:\n\n• Диагностика - 2000р\n• Чип-тюнинг - 5000р\n• Прошивка ЭБУ - 4500р\n• Услуги автоэлектрика"
                                })
                            
                            elif text == "📱 СОЦСЕТИ":
                                message_text = (
                                    "📱 МЫ В СОЦСЕТЯХ:\n\n"
                                    "• Instagram: instagram.com/chiptuning_service_fake\n\n"
                                    f"• <a href='{AVITO_LINK}'>Авито</a> - наши услуги автоэлектрика\n\n"
                                    "Нажмите на 'Авито' для перехода"
                                )
                                requests.post(f"{API_URL}sendMessage", json={
                                    "chat_id": chat_id,
                                    "text": message_text,
                                    "parse_mode": "HTML"
                                })
                            
                            elif text == "📞 КОНТАКТЫ":
                                message_text = (
                                    "📞 НАШИ КОНТАКТЫ:\n\n"
                                    f"• Телефон: {PHONE_NUMBER}\n\n"
                                    f"• <a href='{WHATSAPP_LINK}'>WhatsApp</a>\n"
                                    f"• <a href='{TELEGRAM_LINK}'>Telegram</a>\n\n"
                                    "Нажмите на ссылки для связи"
                                )
                                requests.post(f"{API_URL}sendMessage", json={
                                    "chat_id": chat_id,
                                    "text": message_text,
                                    "parse_mode": "HTML"
                                })
                            
                            elif text == "📍 АДРЕС":
                                requests.post(f"{API_URL}sendMessage", json={
                                    "chat_id": chat_id,
                                    "text": "📍 НАШ АДРЕС:\nул. Пушкина, Дом 9а\n\n🕒 9:00-19:00 ежедневно"
                                })
            
            time.sleep(1)
            
        except requests.exceptions.ConnectionError as e:
            print(f"📡 Ошибка подключения (переподключение через 10с): {e}")
            time.sleep(10)
        except requests.exceptions.Timeout as e:
            print(f"⏰ Таймаут запроса (переподключение через 5с): {e}")
            time.sleep(5)
        except Exception as e:
            print(f"⚠️ Ошибка бота (переподключение через 5с): {e}")
            time.sleep(5)

# Запускаем бота в фоне
threading.Thread(target=telegram_bot, daemon=True).start()

if __name__ == '__main__':
    print("🌐 Запуск Flask сервера...")
    app.run(host='0.0.0.0', port=8080, debug=False)
