#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Тест обработки платежей webhook
"""

import requests
import json

def test_payment_processing():
    """Тест обработки платежей"""
    
    print("🧪 ТЕСТ ОБРАБОТКИ ПЛАТЕЖЕЙ")
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
    print(f"   - sum: {success_data['sum']}")
    print(f"   - payment_status: {success_data['payment_status']}")
    print(f"   - customer_email: {success_data['customer_email']}")
    print()
    
    # Тест 1: Успешная оплата
    print("📋 Тест 1: Успешная оплата")
    print("-" * 40)
    
    headers = {
        'Sign': 'd0b86a63d4f4b3a794022731160e6502b0ff423cf1ce4849c0c740011643efd1'
    }
    
    try:
        response = requests.post("http://localhost:5000/sales/prodamus", data=success_data, headers=headers, timeout=10)
        print(f"   - Status: {response.status_code}")
        print(f"   - Response: {response.text}")
        
        if response.status_code == 200:
            print("   ✅ Успешная оплата обработана!")
        else:
            print("   ❌ Ошибка обработки успешной оплаты")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    print()
    
    # Тест 2: Неудачная оплата
    print("📋 Тест 2: Неудачная оплата")
    print("-" * 40)
    
    failed_data = success_data.copy()
    failed_data['payment_status'] = 'failed'
    failed_data['payment_status_description'] = 'Платеж не прошел'
    
    try:
        response = requests.post("http://localhost:5000/sales/prodamus", data=failed_data, headers=headers, timeout=10)
        print(f"   - Status: {response.status_code}")
        print(f"   - Response: {response.text}")
        
        if response.status_code == 200:
            print("   ✅ Неудачная оплата обработана!")
        else:
            print("   ❌ Ошибка обработки неудачной оплаты")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    print()
    
    # Тест 3: Неверный формат order_id
    print("📋 Тест 3: Неверный формат order_id")
    print("-" * 40)
    
    invalid_data = success_data.copy()
    invalid_data['order_id'] = 'invalid_order_id'
    
    try:
        response = requests.post("http://localhost:5000/sales/prodamus", data=invalid_data, headers=headers, timeout=10)
        print(f"   - Status: {response.status_code}")
        print(f"   - Response: {response.text}")
        
        if response.status_code == 200:
            print("   ✅ Неверный формат order_id обработан!")
        else:
            print("   ❌ Ошибка обработки неверного формата order_id")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
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
    print("   ✅ Проверка обработки успешных платежей")
    print("   ✅ Проверка обработки неудачных платежей")
    print("   ✅ Проверка обработки неверных форматов")
    print("   ✅ Проверка health check")
    print()
    print("🔧 Если все тесты прошли успешно:")
    print("   1. Webhook правильно обрабатывает платежи")
    print("   2. Бот получает уведомления об оплате")
    print("   3. Подписки активируются автоматически")
    print("   4. Система оплаты работает корректно")
    print()
    print("⚠️ ВНИМАНИЕ: Проверка подписи отключена!")
    print("🔧 Это временное решение для тестирования")
    print("📋 После тестирования нужно будет включить проверку подписи")

if __name__ == "__main__":
    test_payment_processing()
