import os
import requests
import time
from flask import Flask
import threading
from datetime import datetime

print("=" * 50)
print("🚗 АВТОСЕРВИС БОТ (ДЕБАГ ВКЛЮЧЁН)")
print("=" * 50)

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Бот работает"

@app.route('/health')
def health():
    return "OK", 200

def telegram_bot():
    print("=" * 50)
    print("🔧 ЗАПУСК ПРОВЕРКИ ТОКЕНА")
    print("=" * 50)
    
    # ========== ПРОВЕРКА ТОКЕНА ==========
    # Способ 1: Стандартный
    TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    print(f"1. os.environ.get: {TOKEN}")
    
    # Способ 2: Альтернативный
    if not TOKEN:
        TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
        print(f"2. os.getenv: {TOKEN}")
    
    # Способ 3: Любая переменная с TOKEN
    if not TOKEN:
        for key, value in os.environ.items():
            if 'TOKEN' in key or 'BOT' in key:
                print(f"3. Найдена переменная: {key}={value[:10]}...")
                TOKEN = value
                break
    
    # ИТОГ проверки
    if not TOKEN:
        print("❌ КРИТИЧЕСКАЯ ОШИБКА: Токен не найден!")
        print("💡 Решение:")
        print("1. Зайди в Koyeb → Settings → Environment Variables")
        print("2. Добавь: Key=TELEGRAM_BOT_TOKEN, Value=твой_токен")
        print("3. Нажми Save и перезапусти сервис")
        return
    
    print(f"✅ Токен найден: {TOKEN[:15]}...")
    
    # ========== ПРОВЕРКА ТОКЕНА ЧЕРЕЗ TELEGRAM API ==========
    print("🔗 Проверяю токен через Telegram API...")
    try:
        test_url = f"https://api.telegram.org/bot{TOKEN}/getMe"
        resp = requests.get(test_url, timeout=10)
        data = resp.json()
        
        if data.get('ok'):
            bot_info = data['result']
            print(f"✅ Токен рабочий!")
            print(f"   🤖 Бот: @{bot_info['username']}")
            print(f"   📛 Имя: {bot_info['first_name']}")
            print(f"   🆔 ID: {bot_info['id']}")
        else:
            print(f"❌ Токен неверный!")
            print(f"   Ошибка: {data.get('description')}")
            print(f"   Код: {data.get('error_code')}")
            return
    except Exception as e:
        print(f"⚠️ Не удалось проверить токен: {type(e).__name__}: {e}")
        # Продолжаем в надежде, что токен рабочий
    
    # ========== ОСНОВНОЙ КОД БОТА ==========
    API_URL = f"https://api.telegram.org/bot{TOKEN}/"
    last_update_id = 0
    message_count = 0
    
    print("=" * 50)
    print("🤖 ЗАПУСКАЮ ОСНОВНОЙ ЦИКЛ БОТА")
    print("=" * 50)
    
    while True:
        try:
            # Запрос обновлений
            resp = requests.get(
                f"{API_URL}getUpdates",
                params={
                    "offset": last_update_id + 1,
                    "timeout": 10,  # Увеличил для стабильности
                    "limit": 100
                },
                timeout=15
            )
            
            if resp.status_code == 200:
                data = resp.json()
                if data.get("ok"):
                    updates = data.get("result", [])
                    
                    if updates:
                        print(f"📦 Получено обновлений: {len(updates)}")
                        
                        for update in updates:
                            last_update_id = update["update_id"]
                            message_count += 1
                            
                            if "message" in update:
                                chat_id = update["message"]["chat"]["id"]
                                text = update["message"].get("text", "").strip()
                                
                                print(f"📩 [#{message_count}] Сообщение: '{text}'")
                                
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
                                        "text": "🚗 Добро пожаловать в автосервис!\n👇 Выберите раздел:",
                                        "reply_markup": keyboard
                                    }, timeout=5)
                                    print("✅ Отправлено: Приветствие")
                                
                                # МЕНЮ
                                elif "📋" in text or "меню" in text.lower():
                                    requests.post(f"{API_URL}sendMessage", json={
                                        "chat_id": chat_id,
                                        "text": "🔧 НАШИ УСЛУГИ:\n\n• Диагностика - 2000р\n• Чип-тюнинг - 5000р\n• Прошивка ЭБУ - 4500р\n• Услуги автоэлектрика"
                                    }, timeout=5)
                                    print("✅ Отправлено: Меню")
                                
                                # СОЦСЕТИ
                                elif "📱" in text or "соцсети" in text.lower():
                                    requests.post(f"{API_URL}sendMessage", json={
                                        "chat_id": chat_id,
                                        "text": "📱 МЫ В СОЦСЕТЯХ:\n\n• Instagram: https://www.instagram.com/auto_uzist_kiz?utm_source=qr&igsh=d203cnZwMDF0eHV4"
                                    }, timeout=5)
                                    print("✅ Отправлено: Соцсети")
                                
                                # КОНТАКТЫ
                                elif "📞" in text or "контакт" in text.lower() or "номера" in text.lower():
                                    requests.post(f"{API_URL}sendMessage", json={
                                        "chat_id": chat_id,
                                        "text": (
                                            "📞 НАШИ КОНТАКТЫ:\n\n"
                                            "• Телефон: +7 922 433-35-45\n\n"
                                            "• WhatsApp: https://wa.me/79224333545\n"
                                            "• Telegram: https://t.me/+79224333545\n"
                                            "• Авито: https://www.avito.ru/kizilyurt/predlozheniya_uslug/avtoelektrik_diagnost_7856909160"
                                        )
                                    }, timeout=5)
                                    print("✅ Отправлено: Контакты")
                                
                                # АДРЕС
                                elif "📍" in text or "адрес" in text.lower():
                                    requests.post(f"{API_URL}sendMessage", json={
                                        "chat_id": chat_id,
                                        "text": (
                                            "📍 НАШ АДРЕС:\n"
                                            "Кизилюрт, ул. Аскерханова 69\n\n"
                                            "🗺️ Google Карты: https://share.google/aHKUZYfsRCtAVFY32\n\n"
                                            "🕒 9:00-19:00 ежедневно"
                                        )
                                    }, timeout=5)
                                    print("✅ Отправлено: Адрес")
                    else:
                        # Если нет обновлений, ждём немного
                        time.sleep(0.5)
                else:
                    print(f"⚠️ Telegram API вернул ошибку: {data}")
                    time.sleep(5)
            else:
                print(f"⚠️ HTTP ошибка: {resp.status_code}")
                time.sleep(5)
                
        except requests.exceptions.Timeout:
            print("⏰ Таймаут запроса (нормально для long polling)")
            time.sleep(1)
        except requests.exceptions.ConnectionError as e:
            print(f"📡 Ошибка соединения: {e}")
            time.sleep(5)
        except Exception as e:
            print(f"❌ Неожиданная ошибка: {type(e).__name__}: {e}")
            time.sleep(5)

# Запускаем бота в отдельном потоке
bot_thread = threading.Thread(target=telegram_bot, daemon=True)
bot_thread.start()

if __name__ == '__main__':
    print("🌐 Запуск Flask сервера...")
    print("=" * 50)
    print("СЕРВИС АКТИВЕН")
    print(f"Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)
