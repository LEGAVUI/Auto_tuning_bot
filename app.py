import os
import requests
import time
from flask import Flask
import threading

print("=" * 50)
print("🚗 АВТОСЕРВИС БОТ (ДЕБАГ РЕЖИМ)")
print("=" * 50)

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Бот работает"

@app.route('/health')
def health():
    return "OK", 200

def telegram_bot():
    # Получаем токен
    TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    if not TOKEN:
        print("❌ Токен не найден")
        return
    
    print(f"✅ Токен: {TOKEN[:10]}...")
    API_URL = f"https://api.telegram.org/bot{TOKEN}/"
    
    last_update_id = 0
    
    print("🤖 Бот запущен. Ожидание сообщений...")
    
    while True:
        try:
            resp = requests.get(
                f"{API_URL}getUpdates",
                params={"offset": last_update_id + 1, "timeout": 1},
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
                            
                            # ========== ДЕБАГ ВЫВОД ==========
                            print("\n" + "="*50)
                            print(f"📩 СООБЩЕНИЕ ОТ ПОЛЬЗОВАТЕЛЯ:")
                            print(f"Текст: '{text}'")
                            print(f"Длина: {len(text)}")
                            print(f"Коды символов: {[ord(c) for c in text]}")
                            print("="*50 + "\n")
                            # ================================
                            
                            # /start
                            if "/start" in text.lower():
                                keyboard = {
                                    "keyboard": [
                                        [{"text": "📋 МЕНЮ"}],
                                        [{"text": "📱 СОЦСЕТИ"}],
                                        [{"text": "📞 КОНТАКТЫ"}],
                                        [{"text": "📍 АДРЕС"}]
                                    ],
                                    "resize_keyboard": True
                                }
                                requests.post(f"{API_URL}sendMessage", json={
                                    "chat_id": chat_id,
                                    "text": "🚗 Добро пожаловать!\n👇 Выберите:",
                                    "reply_markup": keyboard
                                }, timeout=2)
                                continue
                            
                            # УНИВЕРСАЛЬНАЯ ПРОВЕРКА
                            text_lower = text.lower()
                            
                            # 1. МЕНЮ
                            if "меню" in text_lower or "📋" in text:
                                print("✅ Обрабатываю: МЕНЮ")
                                requests.post(f"{API_URL}sendMessage", json={
                                    "chat_id": chat_id,
                                    "text": "🔧 НАШИ УСЛУГИ:\n\n• Диагностика - 2000р\n• Чип-тюнинг - 5000р\n• Прошивка ЭБУ - 4500р\n• Услуги автоэлектрика"
                                }, timeout=2)
                            
                            # 2. СОЦСЕТИ
                            elif "соцсети" in text_lower or "📱" in text:
                                print("✅ Обрабатываю: СОЦСЕТИ")
                                requests.post(f"{API_URL}sendMessage", json={
                                    "chat_id": chat_id,
                                    "text": "📱 МЫ В СОЦСЕТЯХ:\n\n• Instagram: instagram.com/chiptuning_service_fake\n\n• Авито: https://www.avito.ru/avtoelektrik_diagnost_7856909160"
                                }, timeout=2)
                            
                            # 3. КОНТАКТЫ
                            elif "контакт" in text_lower or "📞" in text:
                                print("✅ Обрабатываю: КОНТАКТЫ")
                                requests.post(f"{API_URL}sendMessage", json={
                                    "chat_id": chat_id,
                                    "text": "📞 НАШИ КОНТАКТЫ:\n\n• Телефон: +7 922 433-35-45\n\n• WhatsApp: wa.me/79224333545\n• Telegram: t.me/+79224333545"
                                }, timeout=2)
                            
                            # 4. АДРЕС
                            elif "адрес" in text_lower or "📍" in text:
                                print("✅ Обрабатываю: АДРЕС")
                                requests.post(f"{API_URL}sendMessage", json={
                                    "chat_id": chat_id,
                                    "text": "📍 НАШ АДРЕС:\nул. Пушкина, Дом 9а\n\n🕒 9:00-19:00 ежедневно"
                                }, timeout=2)
                            
                            else:
                                print(f"❓ Неизвестная команда: '{text}'")
            
        except Exception as e:
            print(f"⚠️ Ошибка: {e}")
            time.sleep(1)

# Запускаем бота
threading.Thread(target=telegram_bot, daemon=True).start()

if __name__ == '__main__':
    print("🌐 Flask сервер запускается...")
    app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)
