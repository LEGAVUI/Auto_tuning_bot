import os
import requests
import time
from flask import Flask
import threading

print("=" * 50)
print("🚗 АВТОСЕРВИС БОТ (СТРОГАЯ ЗАЩИТА ОТ ДУБЛИКАТОВ)")
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
        return
    
    API_URL = f"https://api.telegram.org/bot{TOKEN}/"
    last_update_id = 0
    last_response_time = {}  # Время последнего ответа для каждого чата
    
    print("⚡ Бот запущен (анти-дубль режим)")
    
    while True:
        try:
            resp = requests.get(
                f"{API_URL}getUpdates",
                params={"offset": last_update_id + 1, "timeout": 0.5},
                timeout=1
            )
            
            if resp.status_code == 200:
                data = resp.json()
                if data.get("ok"):
                    updates = data.get("result", [])
                    
                    for update in updates:
                        update_id = update["update_id"]
                        
                        # Важно: обновляем last_update_id сразу
                        if update_id > last_update_id:
                            last_update_id = update_id
                        
                        if "message" in update:
                            chat_id = update["message"]["chat"]["id"]
                            message_id = update["message"]["message_id"]
                            text = update["message"].get("text", "").strip().lower()
                            
                            print(f"📩 Chat:{chat_id} Msg:{message_id} Text:{text[:30]}")
                            
                            # Проверяем время последнего ответа в этом чате
                            current_time = time.time()
                            last_time = last_response_time.get(chat_id, 0)
                            
                            # Если прошло меньше 1 секунды с последнего ответа - пропускаем
                            if current_time - last_time < 1.0:
                                print(f"⏸️  Пропуск (тайм-аут): {text[:20]}")
                                continue
                            
                            # Обновляем время ответа для этого чата
                            last_response_time[chat_id] = current_time
                            
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
                                }, timeout=1)
                                print(f"✅ Отправлено приветствие в чат {chat_id}")
                            
                            # МЕНЮ
                            elif "меню" in text or "📋" in text:
                                menu_text = (
                                    "🔧 <b>НАШИ УСЛУГИ:</b>\n\n"
                                    "<b>Ремонт двигателя</b>\n"
                                    "__________________\n"
                                    "Диагностика двигателя    500 ₽\n\n"
                                    "<b>Ремонт электрооборудования</b>\n"
                                    "__________________\n"
                                    "Ремонт датчиков    от 500 ₽\n"
                                    "Ремонт стеклоподъёмника    от 1 000 ₽\n"
                                    "Замена проводки    от 3 000 ₽\n\n"
                                    "<b>Диагностика авто</b>\n"
                                    "__________________\n"
                                    "Комплексная диагностика    от 1 000 ₽\n"
                                    "Компьютерная диагностика    от 500 ₽\n\n"
                                    "<b>Установка доп. оборудования</b>\n"
                                    "__________________\n"
                                    "В зависимости от сложности\n\n"
                                    "📞 <b>Запись по телефону:</b> +7 922 433-35-45"
                                )
                                requests.post(f"{API_URL}sendMessage", json={
                                    "chat_id": chat_id,
                                    "text": menu_text,
                                    "parse_mode": "HTML"
                                }, timeout=1)
                                print(f"✅ Отправлено меню в чат {chat_id}")
                            
                            # СОЦСЕТИ
                            elif "соцсети" in text or "📱" in text:
                                requests.post(f"{API_URL}sendMessage", json={
                                    "chat_id": chat_id,
                                    "text": "📱 <b>МЫ В СОЦСЕТЯХ:</b>\n\n• Instagram: https://www.instagram.com/auto_uzist_kiz?utm_source=qr&igsh=d203cnZwMDF0eHV4",
                                    "parse_mode": "HTML"
                                }, timeout=1)
                                print(f"✅ Отправлены соцсети в чат {chat_id}")
                            
                            # КОНТАКТЫ
                            elif "контакт" in text or "номера" in text or "📞" in text:
                                contacts_text = (
                                    "📞 <b>НАШИ КОНТАКТЫ:</b>\n\n"
                                    "• <b>Телефон:</b> +7 922 433-35-45\n\n"
                                    "• <a href='https://wa.me/79224333545'>WhatsApp</a>\n"
                                    "• <a href='https://t.me/+79224333545'>Telegram</a>\n"
                                    "• <a href='https://www.avito.ru/kizilyurt/predlozheniya_uslug/avtoelektrik_diagnost_7856909160'>Авито</a>"
                                )
                                requests.post(f"{API_URL}sendMessage", json={
                                    "chat_id": chat_id,
                                    "text": contacts_text,
                                    "parse_mode": "HTML",
                                    "disable_web_page_preview": True
                                }, timeout=1)
                                print(f"✅ Отправлены контакты в чат {chat_id}")
                            
                            # АДРЕС
                            elif "адрес" in text or "📍" in text:
                                address_text = (
                                    "📍 <b>НАШ АДРЕС:</b>\n"
                                    "Кизилюрт, ул. Аскерханова 69\n\n"
                                    "🗺️ <a href='https://share.google/aHKUZYfsRCtAVFY32'>Google Карты</a>\n\n"
                                    "🕒 <b>Режим работы:</b> 9:00-19:00 ежедневно"
                                )
                                requests.post(f"{API_URL}sendMessage", json={
                                    "chat_id": chat_id,
                                    "text": address_text,
                                    "parse_mode": "HTML",
                                    "disable_web_page_preview": True
                                }, timeout=1)
                                print(f"✅ Отправлен адрес в чат {chat_id}")
            
        except requests.exceptions.Timeout:
            pass
        except Exception as e:
            print(f"⚠️ Ошибка: {e}")
            time.sleep(0.1)

threading.Thread(target=telegram_bot, daemon=True).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)
