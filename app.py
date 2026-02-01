import os
import requests
import time
from flask import Flask
import threading
from datetime import datetime

print("=" * 50)
print("🚗 АВТОСЕРВИС БОТ (ТУРБО РЕЖИМ)")
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
    TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    
    if not TOKEN:
        print("❌ Токен не найден")
        return
    
    print(f"✅ Токен найден: {TOKEN[:15]}...")
    
    # Проверка токена
    try:
        test_url = f"https://api.telegram.org/bot{TOKEN}/getMe"
        resp = requests.get(test_url, timeout=5)
        if resp.json().get('ok'):
            print(f"✅ Бот: @{resp.json()['result']['username']}")
        else:
            print("❌ Токен неверный")
            return
    except:
        print("⚠️ Проверка токена пропущена")
    
    API_URL = f"https://api.telegram.org/bot{TOKEN}/"
    
    # ========== УЛЬТРА-БЫСТРЫЙ ЦИКЛ ==========
    last_update_id = 0
    message_count = 0
    
    print("⚡ Бот запущен в ТУРБО-РЕЖИМЕ")
    print("=" * 50)
    
    while True:
        try:
            # БЫСТРЫЙ запрос (500ms вместо 10 секунд!)
            resp = requests.get(
                f"{API_URL}getUpdates",
                params={
                    "offset": last_update_id + 1,
                    "timeout": 0.5,  # 500ms!
                    "limit": 10
                },
                timeout=1
            )
            
            if resp.status_code == 200:
                data = resp.json()
                if data.get("ok"):
                    updates = data.get("result", [])
                    
                    if updates:
                        print(f"⚡ Получено {len(updates)} сообщ.")
                        
                        for update in updates:
                            last_update_id = update["update_id"]
                            message_count += 1
                            
                            if "message" in update:
                                chat_id = update["message"]["chat"]["id"]
                                text = update["message"].get("text", "").strip().lower()
                                
                                start_time = time.time()
                                
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
                                        "text": "🚗 Добро пожаловать!",
                                        "reply_markup": keyboard
                                    }, timeout=1)
                                    print(f"✅ Старт за {time.time()-start_time:.2f}с")
                                
                                # МЕНЮ
                                elif "меню" in text or "📋" in text:
                                    requests.post(f"{API_URL}sendMessage", json={
                                        "chat_id": chat_id,
                                        "text": "🔧 Услуги:\n• Диагностика - 2000р\n• Чип-тюнинг - 5000р\n• Прошивка ЭБУ - 4500р"
                                    }, timeout=1)
                                    print(f"✅ Меню за {time.time()-start_time:.2f}с")
                                
                                # СОЦСЕТИ
                                elif "соцсети" in text or "📱" in text:
                                    requests.post(f"{API_URL}sendMessage", json={
                                        "chat_id": chat_id,
                                        "text": "📱 Instagram:\nhttps://www.instagram.com/auto_uzist_kiz"
                                    }, timeout=1)
                                    print(f"✅ Соцсети за {time.time()-start_time:.2f}с")
                                
                                # КОНТАКТЫ
                                elif "контакт" in text or "номера" in text or "📞" in text:
                                    requests.post(f"{API_URL}sendMessage", json={
                                        "chat_id": chat_id,
                                        "text": "📞 Контакты:\n+7 922 433-35-45\nWhatsApp: wa.me/79224333545"
                                    }, timeout=1)
                                    print(f"✅ Контакты за {time.time()-start_time:.2f}с")
                                
                                # АДРЕС
                                elif "адрес" in text or "📍" in text:
                                    requests.post(f"{API_URL}sendMessage", json={
                                        "chat_id": chat_id,
                                        "text": "📍 Адрес:\nКизилюрт, ул. Аскерханова 69\nКарты: share.google/aHKUZYfsRCtAVFY32"
                                    }, timeout=1)
                                    print(f"✅ Адрес за {time.time()-start_time:.2f}с")
                else:
                    time.sleep(0.05)
            else:
                time.sleep(0.05)
                
        except requests.exceptions.Timeout:
            pass
        except requests.exceptions.ConnectionError:
            time.sleep(1)
        except Exception as e:
            print(f"⚠️ Ошибка: {type(e).__name__}")
            time.sleep(1)

# Запускаем бота
threading.Thread(target=telegram_bot, daemon=True).start()

if __name__ == '__main__':
    print("🌐 Сервер запущен")
    app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)
