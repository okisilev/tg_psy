#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Тест webhook с IP адресом
"""

import requests
import json

def test_ip_webhook():
    """Тест webhook с IP адресом"""
    
    print("🧪 ТЕСТ WEBHOOK С IP АДРЕСОМ")
    print("=" * 50)
    
    # Тестовые данные для успешной оплаты
    success_data = {
        'date': '2025-09-22T09:52:32+03:00',
        'order_id': '36086288',
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
    
    # Тест 1: Локальный сервер
    print("📋 Тест 1: Локальный сервер")
    print("-" * 40)
    
    try:
        response = requests.post("http://localhost:5000/sales/prodamus", data=success_data, timeout=5)
        print(f"   - Status: {response.status_code}")
        print(f"   - Response: {response.text}")
        
        if response.status_code == 200:
            print("   ✅ Локальный сервер работает!")
        else:
            print("   ❌ Локальный сервер не работает")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    print()
    
    # Тест 2: Внешний IP адрес
    print("📋 Тест 2: Внешний IP адрес")
    print("-" * 40)
    
    try:
        response = requests.post("http://82.147.71.244:5000/sales/prodamus", data=success_data, timeout=10)
        print(f"   - Status: {response.status_code}")
        print(f"   - Response: {response.text}")
        
        if response.status_code == 200:
            print("   ✅ Внешний IP работает!")
        else:
            print("   ❌ Внешний IP не работает")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    print()
    
    # Тест 3: Health check
    print("📋 Тест 3: Health check")
    print("-" * 40)
    
    try:
        response = requests.get("http://82.147.71.244:5000/health", timeout=10)
        print(f"   - Status: {response.status_code}")
        print(f"   - Response: {response.text}")
        
        if response.status_code == 200:
            print("   ✅ Health check работает!")
        else:
            print("   ❌ Health check не работает")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    print()
    
    # Тест 4: Тест с подписью
    print("📋 Тест 4: Тест с подписью")
    print("-" * 40)
    
    headers = {
        'Sign': 'd0b86a63d4f4b3a794022731160e6502b0ff423cf1ce4849c0c740011643efd1'
    }
    
    try:
        response = requests.post("http://82.147.71.244:5000/sales/prodamus", data=success_data, headers=headers, timeout=10)
        print(f"   - Status: {response.status_code}")
        print(f"   - Response: {response.text}")
        
        if response.status_code == 200:
            print("   ✅ Webhook с подписью работает!")
        else:
            print("   ❌ Webhook с подписью не работает")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    print()
    print("🎉 ТЕСТ ЗАВЕРШЕН!")
    print()
    print("📝 РЕЗУЛЬТАТ:")
    print("   ✅ Проверка webhook с IP адресом")
    print("   ✅ Тестирование локального и внешнего сервера")
    print("   ✅ Проверка health check")
    print("   ✅ Тестирование с подписью")
    print()
    print("🔧 Если все тесты прошли успешно:")
    print("   1. Prodamus сможет отправлять уведомления")
    print("   2. Подписки будут активироваться автоматически")
    print("   3. Система оплаты будет работать")
    print()
    print("⚠️ ВНИМАНИЕ: Используется IP адрес вместо PageKite!")
    print("🔧 Это временное решение для тестирования")

if __name__ == "__main__":
    test_ip_webhook()
