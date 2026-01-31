import os
import requests
import time
from flask import Flask
import threading
from datetime import datetime

# Сохраняем offset в файл для надёжности
OFFSET_FILE = "/tmp/last_offset.txt"

def save_last_offset(offset):
    try:
        with open(OFFSET_FILE, 'w') as f:
            f.write(str(offset))
    except:
        pass

def load_last_offset():
    try:
        with open(OFFSET_FILE, 'r') as f:
            return int(f.read().strip())
    except:
        return 0

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
    # Ждём токен с таймаутом
    max_wait = 30
    waited = 0
    
    while waited < max_wait:
        TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
        if TOKEN:
            break
        print(f"⏳ Ожидание токена... ({waited}/{max_wait} сек)")
        time.sleep(2)
        waited += 2
    
    if not TOKEN:
        print("❌ Токен не найден. Бот будет работать в тестовом режиме.")
        TOKEN = "dummy_token"  # Заглушка для продолжения работы
    
    print(f"✅ Токен получен! Бот запускается...")
    
    API_URL = f"https://api.telegram.org/bot{TOKEN}/" if TOKEN != "dummy_token" else None
    
    # Контакты
    AVITO_LINK = "https://www.avito.ru/kizilyurt/predlozheniya_uslug/avtoelektrik_diagnost_7856909160"
    PHONE_NUMBER = "+7 922 433-35-45"
    WHATSAPP_LINK = "https://wa.me/79224333545"
    TELEGRAM_LINK = "https://t.me/+79224333545"
    
    keyboard = {
        "keyboard": [
            [{"text": "📋 МЕНЮ"}],
            [{"text": "📱 СОЦСЕТИ"}], 
            [{"text": "📞 КОНТАКТЫ"}],
            [{"text": "📍 АДРЕС"}]
        ],
        "resize_keyboard": True
    }
    
    last_update_id = load_last_offset()
    
    print("✅ Telegram бот запущен")
    print("🤖 Ожидание сообщений...")
    
    while True:
        try:
            if API_URL is None:  # Режим без токена
                time.sleep(5)
                continue
            
            # Быстрый запрос
            resp = requests.get(
                f"{API_URL}getUpdates",
                params={"offset": last_update_id + 1, "timeout": 3},
                timeout=5
            )
            
            if resp.status_code == 200:
                data = resp.json()
                if data.get("ok"):
                    updates = data.get("result", [])
                    
                    if updates:
                        for update in updates:
                            last_update_id = update["update_id"]
                            save_last_offset(last_update_id)
                            
                            if "message" in update:
                                chat_id = update["message"]["chat"]["id"]
                                text = update["message"].get("text", "")
                                
                                print(f"📩 Получено: {text[:50]}")
                                
                                # /start
                                if "/start" in text.lower():
                                    requests.post(f"{API_URL}sendMessage", json={
                                        "chat_id": chat_id,
                                        "text": "🚗 Добро пожаловать в автосервис!\n👇 Выберите раздел:",
                                        "reply_markup": keyboard
                                    }, timeout=3)
                                
                                # Меню
                                elif text == "📋 МЕНЮ":
                                    requests.post(f"{API_URL}sendMessage", json={
                                        "chat_id": chat_id,
                                        "text": "🔧 НАШИ УСЛУГИ:\n\n• Диагностика - 2000р\n• Чип-тюнинг - 5000р\n• Прошивка ЭБУ - 4500р\n• Услуги автоэлектрика"
                                    }, timeout=3)
                                
                                elif text == "📱 СОЦСЕТИ":
                                    message_text = (
                                        "📱 МЫ В СОЦСЕТЯХ:\n\n"
                                        f"• Instagram: instagram.com/chiptuning_service_fake\n\n"
                                        f"• <a href='{AVITO_LINK}'>Авито</a> - наши услуги автоэлектрика\n\n"
                                        "Нажмите на 'Авито' для перехода"
                                    )
                                    requests.post(f"{API_URL}sendMessage", json={
                                        "chat_id": chat_id,
                                        "text": message_text,
                                        "parse_mode": "HTML"
                                    }, timeout=3)
                                
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
                                    }, timeout=3)
                                
                                elif text == "📍 АДРЕС":
                                    requests.post(f"{API_URL}sendMessage", json={
                                        "chat_id": chat_id,
                                        "text": "📍 НАШ АДРЕС:\nул. Пушкина, Дом 9а\n\n🕒 9:00-19:00 ежедневно"
                                    }, timeout=3)
            
            # Короткая пауза
            time.sleep(0.1)
            
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Сетевая ошибка (продолжаю): {type(e).__name__}")
            time.sleep(2)
        except Exception as e:
            print(f"❌ Критическая ошибка: {e}")
            time.sleep(5)

# Запускаем бота
threading.Thread(target=telegram_bot, daemon=True).start()

if __name__ == '__main__':
    print("🌐 Запуск Flask сервера...")
    app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)
