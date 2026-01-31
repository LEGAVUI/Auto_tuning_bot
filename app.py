import os
import requests
import time
from flask import Flask
import threading

print("=" * 50)
print("🚗 АВТОСЕРВИС БОТ (ФИНАЛЬНАЯ ВЕРСИЯ)")
print("=" * 50)

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Бот работает"

@app.route('/health')
def health():
    return "OK", 200

def telegram_bot():
    TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    if not TOKEN:
        print("❌ Токен не найден")
        return
    
    API_URL = f"https://api.telegram.org/bot{TOKEN}/"
    last_update_id = 0
    
    print("🤖 Бот запущен. Ожидание сообщений...")
    
    # Словарь ответов с HTML-разметкой
    responses = {
        "меню": "🔧 <b>НАШИ УСЛУГИ:</b>\n\n• Диагностика - 2000р\n• Чип-тюнинг - 5000р\n• Прошивка ЭБУ - 4500р\n• Услуги автоэлектрика",
        
        "соцсети": (
            "📱 <b>МЫ В СОЦСЕТЯХ:</b>\n\n"
            "• <a href='https://www.instagram.com/auto_uzist_kiz?utm_source=qr&igsh=d203cnZwMDF0eHV4'>Instagram</a> - подписывайтесь!"
        ),
        
        "контакт": (
            "📞 <b>НАШИ КОНТАКТЫ:</b>\n\n"
            "• Телефон: +7 922 433-35-45\n\n"
            "• <a href='https://wa.me/79224333545'>WhatsApp</a>\n"
            "• <a href='https://t.me/+79224333545'>Telegram</a>\n"
            "• <a href='https://www.avito.ru/kizilyurt/predlozheniya_uslug/avtoelektrik_diagnost_7856909160'>Авито</a>"
        ),
        
        "адрес": (
            "📍 <b>НАШ АДРЕС:</b>\n"
            "Кизилюрт, ул. Аскерханова 69\n\n"
            "<a href='https://share.google/aHKUZYfsRCtAVFY32'>🗺️ Открыть в Google Картах</a>\n\n"
            "🕒 9:00-19:00 ежедневно"
        ),
        
        "номера": (  # Для "НОМЕРА ДЛЯ СВЯЗИ"
            "📞 <b>НАШИ КОНТАКТЫ:</b>\n\n"
            "• Телефон: +7 922 433-35-45\n\n"
            "• <a href='https://wa.me/79224333545'>WhatsApp</a>\n"
            "• <a href='https://t.me/+79224333545'>Telegram</a>\n"
            "• <a href='https://www.avito.ru/kizilyurt/predlozheniya_uslug/avtoelektrik_diagnost_7856909160'>Авито</a>"
        ),
        
        "адреса": (  # Для "АДРЕСА"
            "📍 <b>НАШ АДРЕС:</b>\n"
            "Кизилюрт, ул. Аскерханова 69\n\n"
            "<a href='https://share.google/aHKUZYfsRCtAVFY32'>🗺️ Открыть в Google Картах</a>\n\n"
            "🕒 9:00-19:00 ежедневно"
        )
    }
    
    while True:
        try:
            resp = requests.get(
                f"{API_URL}getUpdates",
                params={"offset": last_update_id + 1, "timeout": 1},
                timeout=3
            )
            
            if resp.status_code == 200:
                data = resp.json()
                if data.get("ok"):
                    updates = data.get("result", [])
                    
                    for update in updates:
                        last_update_id = update["update_id"]
                        
                        if "message" in update:
                            chat_id = update["message"]["chat"]["id"]
                            text = update["message"].get("text", "").strip().lower()
                            
                            print(f"📩 Получено: {text}")
                            
                            # /start
                            if "/start" in text:
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
                                    "text": "🚗 Добро пожаловать в автосервис!\n👇 Выберите раздел:",
                                    "reply_markup": keyboard
                                }, timeout=3)
                                continue
                            
                            # Определяем ответ
                            response_text = None
                            parse_mode = None
                            
                            if "меню" in text or "📋" in text:
                                response_text = responses["меню"]
                                print("✅ Отправляю: МЕНЮ")
                            
                            elif "соцсети" in text or "📱" in text:
                                response_text = responses["соцсети"]
                                parse_mode = "HTML"
                                print("✅ Отправляю: СОЦСЕТИ")
                            
                            elif "контакт" in text or "номера" in text or "📞" in text or "связи" in text:
                                response_text = responses["контакт"]
                                parse_mode = "HTML"
                                print("✅ Отправляю: КОНТАКТЫ")
                            
                            elif "адрес" in text or "📍" in text:
                                response_text = responses["адрес"]
                                parse_mode = "HTML"
                                print("✅ Отправляю: АДРЕС")
                            
                            # Отправляем ответ
                            if response_text:
                                payload = {
                                    "chat_id": chat_id,
                                    "text": response_text
                                }
                                if parse_mode:
                                    payload["parse_mode"] = parse_mode
                                
                                requests.post(f"{API_URL}sendMessage", 
                                            json=payload, 
                                            timeout=3)
            
        except Exception as e:
            if "timeout" not in str(e).lower():
                print(f"⚠️ Ошибка: {type(e).__name__}")
            time.sleep(1)

# Запускаем бота
threading.Thread(target=telegram_bot, daemon=True).start()

if __name__ == '__main__':
    print("🌐 Flask сервер запускается...")
    app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)
