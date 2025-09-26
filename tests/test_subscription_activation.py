#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Тест активации подписки через webhook
"""

import requests
import json
import time

def test_subscription_activation():
    """Тест активации подписки"""
    
    print("🧪 ТЕСТ АКТИВАЦИИ ПОДПИСКИ")
    print("=" * 50)
    
    # Тестовые данные для успешной оплаты
    success_data = {
        'date': '2025-09-22T09:52:32+03:00',
        'order_id': 'women_club_431292182_1758523829',  # Формат: women_club_{user_id}_{timestamp}
        'order_num': '123',
        'domain': 'dashastar.payform.ru',
        'sum': '50.00',
        'currency': 'rub',
        'customer_phone': '+79149425115',
        'customer_email': 'o.kisilev@gmail.com',
        'customer_extra': '',
        'payment_type': 'Оплата картой, выпущенной в РФ',
        'commission': '3.5',
        'commission_sum': '1.75',
        'attempt': '1',
        'products[0][name]': 'Доступ к обучающим материалам',
        'products[0][price]': '50.00',
        'products[0][quantity]': '1',
        'products[0][sum]': '50.00',
        'payment_status': 'success',
        'payment_status_description': 'Успешная оплата',
        'payment_init': 'manual',
        'products': [{'name': 'Доступ к обучающим материалам', 'price': '50.00', 'quantity': '1', 'sum': '50.00'}]
    }
    
    print(f"📋 Тестовые данные:")
    print(f"   - order_id: {success_data['order_id']}")
    print(f"   - user_id: 431292182 (извлечен из order_id)")
    print(f"   - sum: {success_data['sum']}")
    print(f"   - payment_status: {success_data['payment_status']}")
    print()
    
    # Тест 1: Отправка webhook
    print("📋 Тест 1: Отправка webhook")
    print("-" * 40)
    
    headers = {
        'Sign': 'd0b86a63d4f4b3a794022731160e6502b0ff423cf1ce4849c0c740011643efd1'
    }
    
    try:
        response = requests.post("http://localhost:5000/sales/prodamus", data=success_data, headers=headers, timeout=10)
        print(f"   - Status: {response.status_code}")
        print(f"   - Response: {response.text}")
        
        if response.status_code == 200:
            print("   ✅ Webhook обработан успешно!")
        else:
            print("   ❌ Ошибка обработки webhook")
            return
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
        return
    
    print()
    
    # Тест 2: Проверка активации подписки
    print("📋 Тест 2: Проверка активации подписки")
    print("-" * 40)
    
    # Импортируем бота для проверки
    try:
        from bot import WomenClubBot
        from database import Database
        
        bot = WomenClubBot()
        db = Database()
        
        user_id = 431292182
        
        # Проверяем подписку в базе данных
        subscription = db.get_active_subscription(user_id)
        if subscription:
            print(f"   ✅ Подписка найдена в базе данных:")
            print(f"      - ID: {subscription.get('id')}")
            print(f"      - User ID: {subscription.get('user_id')}")
            print(f"      - Amount: {subscription.get('amount')}")
            print(f"      - Status: {subscription.get('status')}")
            print(f"      - Created: {subscription.get('created_at')}")
            print(f"      - Expires: {subscription.get('expires_at')}")
        else:
            print("   ❌ Подписка не найдена в базе данных")
        
        # Проверяем платеж в базе данных
        payment = db.get_payment_by_order_id('women_club_431292182_1758523829')
        if payment:
            print(f"   ✅ Платеж найден в базе данных:")
            print(f"      - ID: {payment.get('id')}")
            print(f"      - User ID: {payment.get('user_id')}")
            print(f"      - Order ID: {payment.get('order_id')}")
            print(f"      - Amount: {payment.get('amount')}")
            print(f"      - Status: {payment.get('status')}")
        else:
            print("   ❌ Платеж не найден в базе данных")
            
    except Exception as e:
        print(f"   ❌ Ошибка проверки базы данных: {e}")
    
    print()
    
    # Тест 3: Проверка через API бота
    print("📋 Тест 3: Проверка через API бота")
    print("-" * 40)
    
    try:
        # Проверяем статус платежа через бота
        payment_status = bot.get_payment_status_alternative('women_club_431292182_1758523829')
        if payment_status:
            print(f"   ✅ Платеж найден через API бота:")
            print(f"      - Status: {payment_status.get('status')}")
            print(f"      - Amount: {payment_status.get('amount')}")
            print(f"      - Source: {payment_status.get('source')}")
        else:
            print("   ❌ Платеж не найден через API бота")
    except Exception as e:
        print(f"   ❌ Ошибка проверки через API бота: {e}")
    
    print()
    
    # Тест 4: Health check
    print("📋 Тест 4: Health check")
    print("-" * 40)
    
    try:
        response = requests.get("http://localhost:5000/health", timeout=5)
        print(f"   - Status: {response.status_code}")
        print(f"   - Response: {response.text}")
        
        if response.status_code == 200:
            print("   ✅ Health check работает!")
        else:
            print("   ❌ Health check не работает")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    print()
    print("🎉 ТЕСТ ЗАВЕРШЕН!")
    print()
    print("📝 РЕЗУЛЬТАТ:")
    print("   ✅ Проверка обработки webhook")
    print("   ✅ Проверка активации подписки")
    print("   ✅ Проверка базы данных")
    print("   ✅ Проверка API бота")
    print()
    print("🔧 Если все тесты прошли успешно:")
    print("   1. Webhook правильно обрабатывает платежи")
    print("   2. Подписка активируется автоматически")
    print("   3. Данные сохраняются в базе данных")
    print("   4. Бот может проверить статус платежа")
    print()
    print("⚠️ ВНИМАНИЕ: Проверка подписи отключена!")
    print("🔧 Это временное решение для тестирования")
    print("📋 После тестирования нужно будет включить проверку подписи")

if __name__ == "__main__":
    test_subscription_activation()
