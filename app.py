    # ========== УЛЬТРА-БЫСТРЫЙ ЦИКЛ ==========
    last_update_id = 0
    message_count = 0
    
    print("⚡ Бот запущен в РЕЖИМЕ ТУРБО")
    print("=" * 50)
    
    while True:
        try:
            # СУПЕР-БЫСТРЫЙ запрос (вместо 10 секунд - 500ms!)
            resp = requests.get(
                f"{API_URL}getUpdates",
                params={
                    "offset": last_update_id + 1,
                    "timeout": 0.5,  # 500ms вместо 10 секунд!
                    "limit": 10
                },
                timeout=1  # Общий timeout 1 секунда
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
                                text = update["message"].get("text", "").strip()
                                
                                # БЫСТРАЯ обработка
                                start_time = time.time()
                                
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
                                        "text": "🚗 Добро пожаловать!",
                                        "reply_markup": keyboard
                                    }, timeout=1)  # Быстрая отправка
                                    
                                    print(f"✅ Ответ за {time.time()-start_time:.2f}с")
                                
                                # МЕНЮ
                                elif "📋" in text or "меню" in text.lower():
                                    requests.post(f"{API_URL}sendMessage", json={
                                        "chat_id": chat_id,
                                        "text": "🔧 Услуги:\n• Диагностика - 2000р\n• Чип-тюнинг - 5000р\n• Прошивка ЭБУ - 4500р"
                                    }, timeout=1)
                                    print(f"✅ Меню за {time.time()-start_time:.2f}с")
                                
                                # СОЦСЕТИ
                                elif "📱" in text or "соцсети" in text.lower():
                                    requests.post(f"{API_URL}sendMessage", json={
                                        "chat_id": chat_id,
                                        "text": "📱 Instagram:\nhttps://www.instagram.com/auto_uzist_kiz"
                                    }, timeout=1)
                                    print(f"✅ Соцсети за {time.time()-start_time:.2f}с")
                                
                                # КОНТАКТЫ
                                elif "📞" in text or "контакт" in text.lower() or "номера" in text.lower():
                                    requests.post(f"{API_URL}sendMessage", json={
                                        "chat_id": chat_id,
                                        "text": (
                                            "📞 Контакты:\n"
                                            "• +7 922 433-35-45\n"
                                            "• WhatsApp: wa.me/79224333545\n"
                                            "• Telegram: t.me/+79224333545\n"
                                            "• Авито: avito.ru/avtoelektrik_diagnost_7856909160"
                                        )
                                    }, timeout=1)
                                    print(f"✅ Контакты за {time.time()-start_time:.2f}с")
                                
                                # АДРЕС
                                elif "📍" in text or "адрес" in text.lower():
                                    requests.post(f"{API_URL}sendMessage", json={
                                        "chat_id": chat_id,
                                        "text": (
                                            "📍 Адрес:\n"
                                            "Кизилюрт, ул. Аскерханова 69\n"
                                            "🗺️ Карты: share.google/aHKUZYfsRCtAVFY32\n"
                                            "🕒 9:00-19:00"
                                        )
                                    }, timeout=1)
                                    print(f"✅ Адрес за {time.time()-start_time:.2f}с")
                    
                    # НЕТ time.sleep() между запросами - максимальная скорость!
                    # Просто сразу следующий цикл
                else:
                    # Если ошибка API - небольшая пауза
                    time.sleep(0.1)
            else:
                # Если HTTP ошибка - небольшая пауза
                time.sleep(0.1)
                
        except requests.exceptions.Timeout:
            # Таймаут - это нормально в быстром режиме
            pass
        except requests.exceptions.ConnectionError:
            time.sleep(1)
        except Exception as e:
            print(f"⚠️ Ошибка: {type(e).__name__}")
            time.sleep(1)
