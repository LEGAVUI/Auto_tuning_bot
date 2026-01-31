import os
import requests
import time
from flask import Flask
import threading
from datetime import datetime

print("=" * 50)
print("🚗 АВТОСЕРВИС БОТ (СТАБИЛЬНАЯ ВЕРСИЯ)")
print("=" * 50)

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Бот работает"

@app.route('/health')
def health():
    return "OK", 200

# Telegram бот
def telegram_bot():
    # Ждём токен
    for i in range(10):
        TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
        if TOKEN:
            print(f"✅ Токен получен (попытка {i+1})")
            break
        print(f"⏳ Ожидание токена... {i+1}/10")
        time.sleep(2)
    else:
        print("❌ Токен не найден. Бот остановлен.")
        return
    
    API_URL = f"https://api.telegram.org/bot{TOKEN}/"
    
    # Контакты
    AVITO_LINK = "https://www.avito.ru/kizilyurt/predlozheniya_uslug/avtoelektrik_diagnost_7856909160"
    PHONE = "+7 922 433-35-45"
    
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
    error_count = 0
    
    print("🤖 Бот запущен. Ожидание сообщений...")
    
    while True:
        try:
            # ОЧЕНЬ КОРОТКИЙ запрос
            resp = requests.get(
                f"{API_URL}getUpdates",
                params={"offset": last_update_id + 1, "timeout": 1, "limit": 1},
                timeout=2
            )
            
            if resp.status_code == 200:
                data = resp.json()
                if data.get("ok"):
                    updates = data.get("result", [])
                    
                    for update in updates:
                        last_update_id = update["update_id"]
                        
                        if "message" in update:
                            chat_id = update["message"]["chat"]["id"]
                            text = update["message"].get("text", "").strip()
                            
                            print(f"📩 Получено: {text}")
                            
                            # /start
                            if "/start" in text.lower():
                                requests.post(f"{API_URL}sendMessage", json={
                                    "chat_id": chat_id,
                                    "text": "🚗 Добро пожаловать!\n👇 Выберите:",
                                    "reply_markup": keyboard
                                }, timeout=2)
                                continue
                            
                            # Быстрые ответы
                            if text == "📋 МЕНЮ":
                                requests.post(f"{API_URL}sendMessage", json={
                                    "chat_id": chat_id,
                                    "text": "🔧 УСЛУГИ:\n• Диагностика - 2000р\n• Чип-тюнинг - 5000р\n• Прошивка ЭБУ - 4500р"
                                }, timeout=2)
                            
                            elif text == "📱 СОЦСЕТИ":
                                requests.post(f"{API_URL}sendMessage", json={
                                    "chat_id": chat_id,
                                    "text": f"📱 СОЦСЕТИ:\n• Авито: {AVITO_LINK}\n• Instagram: instagram.com/chiptuning_service_fake"
                                }, timeout=2)
                            
                            elif text == "📞 КОНТАКТЫ":
                                requests.post(f"{API_URL}sendMessage", json={
                                    "chat_id": chat_id,
                                    "text": f"📞 КОНТАКТЫ:\n• {PHONE}\n• WhatsApp: wa.me/79224333545\n• Telegram: t.me/+79224333545"
                                }, timeout=2)
                            
                            elif text == "📍 АДРЕС":
                                requests.post(f"{API_URL}sendMessage", json={
                                    "chat_id": chat_id,
                                    "text": "📍 АДРЕС:\nул. Пушкина, 9а\n🕒 9:00-19:00"
                                }, timeout=2)
            
            error_count = 0  # Сброс счётчика ошибок
            
        except requests.exceptions.RequestException as e:
            error_count += 1
            if error_count % 10 == 0:  # Логируем каждую 10-ю ошибку
                print(f"⚠️ Ошибка сети ({error_count}): {type(e).__name__}")
            
            if error_count > 30:  # Если много ошибок подряд
                print("🔄 Перезагрузка из-за множества ошибок...")
                time.sleep(5)
                error_count = 0
            
            time.sleep(0.1)
        
        except Exception as e:
            print(f"❌ Неизвестная ошибка: {e}")
            time.sleep(1)

# Запускаем бота
threading.Thread(target=telegram_bot, daemon=True).start()

if __name__ == '__main__':
    print("🌐 Flask сервер запускается...")
    app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)
