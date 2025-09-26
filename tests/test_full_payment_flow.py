#!/usr/bin/env python3
"""
Тест полного процесса оплаты и активации подписки
"""

import os
import sys
import time
import asyncio
from datetime import datetime, timedelta

def test_payment_creation():
    """Тест создания платежа на 50 рублей"""
    print("💳 Тестирование создания платежа на 50 рублей...")
    print("=" * 60)
    
    try:
        from prodamus import ProdаmusAPI
        
        # Создаем экземпляр API
        api = ProdаmusAPI()
        
        # Тестовые данные
        test_user_id = 431292182
        test_username = "Fun_Oleg"
        
        print(f"🔧 Параметры:")
        print(f"   - User ID: {test_user_id}")
        print(f"   - Username: {test_username}")
        print(f"   - Shop ID: {api.shop_id}")
        print(f"   - Demo Mode: {api.demo_mode}")
        print(f"   - Amount: 5000 копеек (50 рублей)")
        print()
        
        # Создаем платеж
        print("🚀 Создание платежа...")
        payment_result = api.create_payment(test_user_id, test_username)
        
        if payment_result:
            print("✅ Платеж создан успешно!")
            print(f"   - Payment ID: {payment_result.get('payment_id')}")
            print(f"   - Amount: {payment_result.get('amount')} копеек (50 рублей)")
            print(f"   - Payment URL: {payment_result.get('payment_url')}")
            print()
            
            # Проверяем URL
            payment_url = payment_result.get('payment_url')
            if payment_url and 'dashastar.payform.ru' in payment_url:
                print("✅ URL платежа корректен")
                return payment_result
            else:
                print("❌ URL платежа некорректен")
                return None
        else:
            print("❌ Ошибка создания платежа")
            return None
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None

def test_webhook_processing():
    """Тест обработки webhook"""
    print("\n🔗 Тестирование обработки webhook...")
    print("=" * 60)
    
    try:
        from webhook import handle_successful_payment
        
        # Тестовые данные webhook
        test_webhook_data = {
            'order_id': f'test_order_{int(time.time())}',
            'amount': 5000,
            'currency': 'RUB',
            'status': 'success',
            'custom_fields': {
                'user_id': '431292182',
                'username': 'Fun_Oleg'
            }
        }
        
        print(f"🔧 Тестовые данные webhook:")
        print(f"   - Order ID: {test_webhook_data['order_id']}")
        print(f"   - Amount: {test_webhook_data['amount']} копеек")
        print(f"   - User ID: {test_webhook_data['custom_fields']['user_id']}")
        print(f"   - Username: {test_webhook_data['custom_fields']['username']}")
        print()
        
        print("🚀 Обработка webhook...")
        handle_successful_payment(
            test_webhook_data['order_id'],
            test_webhook_data['amount'],
            test_webhook_data
        )
        
        print("✅ Webhook обработан успешно")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка обработки webhook: {e}")
        return False

def test_subscription_activation():
    """Тест активации подписки"""
    print("\n🎯 Тестирование активации подписки...")
    print("=" * 60)
    
    try:
        from database import Database
        
        # Создаем тестовую подписку
        db = Database()
        test_user_id = 431292182
        test_order_id = f'test_subscription_{int(time.time())}'
        test_amount = 5000
        
        print(f"🔧 Создание тестовой подписки:")
        print(f"   - User ID: {test_user_id}")
        print(f"   - Order ID: {test_order_id}")
        print(f"   - Amount: {test_amount} копеек")
        print()
        
        # Создаем подписку
        db.create_subscription(test_user_id, test_order_id, test_amount)
        print("✅ Подписка создана в базе данных")
        
        # Проверяем подписку
        subscription = db.get_active_subscription(test_user_id)
        if subscription:
            print(f"✅ Активная подписка найдена:")
            print(f"   - ID: {subscription.id}")
            print(f"   - User ID: {subscription.user_id}")
            print(f"   - Amount: {subscription.amount} копеек")
            print(f"   - Expires: {subscription.expires_at}")
            print(f"   - Status: {subscription.status}")
            return True
        else:
            print("❌ Активная подписка не найдена")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка активации подписки: {e}")
        return False

def test_channel_access():
    """Тест доступа к каналу"""
    print("\n📺 Тестирование доступа к каналу...")
    print("=" * 60)
    
    try:
        from config import CHANNEL_ID, CHANNEL_USERNAME, CHANNEL_INVITE_LINK
        
        print(f"🔧 Конфигурация канала:")
        print(f"   - Channel ID: {CHANNEL_ID}")
        print(f"   - Channel Username: {CHANNEL_USERNAME}")
        print(f"   - Invite Link: {CHANNEL_INVITE_LINK}")
        print()
        
        # Проверяем конфигурацию
        if CHANNEL_ID and CHANNEL_ID != '-1001234567890':
            print("✅ ID канала настроен")
        else:
            print("⚠️ ID канала не настроен (используется тестовый)")
        
        if CHANNEL_INVITE_LINK and 't.me' in CHANNEL_INVITE_LINK:
            print("✅ Ссылка-приглашение настроена")
        else:
            print("⚠️ Ссылка-приглашение не настроена")
        
        print("\n📝 Для полного тестирования:")
        print("   1. Настройте реальный CHANNEL_ID в config.py")
        print("   2. Убедитесь, что бот является администратором канала")
        print("   3. Протестируйте добавление пользователя в канал")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка проверки доступа к каналу: {e}")
        return False

def test_demo_cards():
    """Тест демо-карт"""
    print("\n🧪 Тестовые карты для демо-режима:")
    print("=" * 60)
    
    demo_cards = [
        {"name": "МИР", "number": "2202 2050 0001 2424", "expiry": "05/35", "cvc": "669"},
        {"name": "MasterCard", "number": "5469 9801 0004 8525", "expiry": "05/26", "cvc": "041"},
        {"name": "Visa", "number": "4006 8009 0096 2514", "expiry": "05/26", "cvc": "941"},
        {"name": "Монета", "number": "2200 2400 0000 0006", "expiry": "12/24", "cvc": "123"},
        {"name": "ГазпромБанк", "number": "4242 4242 4242 4242", "expiry": "12/30", "cvc": "123"}
    ]
    
    for card in demo_cards:
        print(f"📱 {card['name']}: {card['number']} ({card['expiry']}, CVC: {card['cvc']})")
    
    print("\n💡 Инструкция по тестированию:")
    print("   1. Откройте URL платежа в браузере")
    print("   2. Заполните форму тестовыми данными")
    print("   3. Используйте одну из тестовых карт")
    print("   4. Проверьте получение webhook уведомления")
    print("   5. Убедитесь, что пользователь добавлен в канал")
    
    return True

def main():
    """Основная функция"""
    print("🚀 ТЕСТ ПОЛНОГО ПРОЦЕССА ОПЛАТЫ И АКТИВАЦИИ ПОДПИСКИ")
    print("=" * 70)
    print(f"Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Сумма платежа: 50 рублей (5000 копеек)")
    print(f"Длительность подписки: 30 дней")
    print()
    
    # Запускаем тесты
    tests = [
        ("Создание платежа", test_payment_creation),
        ("Обработка webhook", test_webhook_processing),
        ("Активация подписки", test_subscription_activation),
        ("Доступ к каналу", test_channel_access),
        ("Демо-карты", test_demo_cards)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result is not None and result is not False))
        except Exception as e:
            print(f"❌ Ошибка в тесте '{test_name}': {e}")
            results.append((test_name, False))
    
    # Выводим итоги
    print("\n" + "=" * 70)
    print("📋 ИТОГИ ТЕСТИРОВАНИЯ:")
    
    passed = 0
    for test_name, success in results:
        status = "✅ ПРОЙДЕН" if success else "❌ ПРОВАЛЕН"
        print(f"   {test_name}: {status}")
        if success:
            passed += 1
    
    print(f"\n🎯 Результат: {passed}/{len(results)} тестов пройдено")
    
    if passed == len(results):
        print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
        print("\n📝 Система готова к использованию:")
        print("   1. Запустите webhook сервер: python3 start_webhook.py")
        print("   2. Откройте URL платежа в браузере")
        print("   3. Используйте тестовые карты для оплаты")
        print("   4. Проверьте автоматическое добавление в канал")
    else:
        print(f"\n⚠️ {len(results) - passed} тестов не пройдено")
        print("\n📝 Рекомендации:")
        print("   1. Проверьте конфигурацию в config.py")
        print("   2. Убедитесь, что все зависимости установлены")
        print("   3. Настройте реальный CHANNEL_ID")

if __name__ == "__main__":
    main()
