#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Тест webhook без проверки подписи
"""

import requests
import json

def test_no_signature():
    """Тест webhook без проверки подписи"""
    
    print("🧪 ТЕСТ WEBHOOK БЕЗ ПРОВЕРКИ ПОДПИСИ")
    print("=" * 50)
    
    # Тестовые данные (как от Prodamus)
    test_data = {
        'date': '2025-09-22T00:00:00+03:00',
        'order_id': '1',
        'order_num': 'test',
        'domain': 'dashastar.payform.ru',
        'sum': '1000.00',
        'customer_phone': '+79999999999',
        'customer_email': 'email@domain.com',
        'customer_extra': 'тест',
        'payment_type': 'Пластиковая карта Visa, MasterCard, МИР',
        'commission': '3.5',
        'commission_sum': '35.00',
        'attempt': '1',
        'sys': 'test',
        'products[0][name]': 'Доступ к обучающим материалам',
        'products[0][price]': '1000.00',
        'products[0][quantity]': '1',
        'products[0][sum]': '1000.00',
        'payment_status': 'success',
        'payment_status_description': 'Успешная оплата',
        'products': [{'name': 'Доступ к обучающим материалам', 'price': '1000.00', 'quantity': '1', 'sum': '1000.00'}]
    }
    
    print(f"📋 Тестовые данные:")
    print(f"   - order_id: {test_data['order_id']}")
    print(f"   - sum: {test_data['sum']}")
    print(f"   - payment_status: {test_data['payment_status']}")
    print(f"   - customer_email: {test_data['customer_email']}")
    print()
    
    # Тест 1: Локальный сервер без подписи
    print("📋 Тест 1: Локальный сервер без подписи")
    print("-" * 50)
    
    try:
        response = requests.post("http://localhost:5000/sales/prodamus", data=test_data, timeout=5)
        print(f"   - Status: {response.status_code}")
        print(f"   - Response: {response.text}")
        
        if response.status_code == 200:
            print("   ✅ Локальный сервер работает без подписи!")
        else:
            print("   ❌ Локальный сервер не работает")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    print()
    
    # Тест 2: Локальный сервер с подписью
    print("📋 Тест 2: Локальный сервер с подписью")
    print("-" * 50)
    
    headers = {
        'Sign': '7e6c5e9e4596d475476c41401f100488522dda04f2871002123d5c72cae3d261'
    }
    
    try:
        response = requests.post("http://localhost:5000/sales/prodamus", data=test_data, headers=headers, timeout=5)
        print(f"   - Status: {response.status_code}")
        print(f"   - Response: {response.text}")
        
        if response.status_code == 200:
            print("   ✅ Локальный сервер работает с подписью!")
        else:
            print("   ❌ Локальный сервер не работает")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    print()
    
    # Тест 3: Удаленный сервер без подписи
    print("📋 Тест 3: Удаленный сервер без подписи")
    print("-" * 50)
    
    url = "https://dashastar.pagekite.me/sales/prodamus"
    
    try:
        response = requests.post(url, data=test_data, timeout=10)
        print(f"   - Status: {response.status_code}")
        print(f"   - Response: {response.text}")
        
        if response.status_code == 200:
            print("   ✅ Удаленный сервер работает без подписи!")
        else:
            print("   ❌ Удаленный сервер не работает")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    print()
    
    # Тест 4: Удаленный сервер с подписью
    print("📋 Тест 4: Удаленный сервер с подписью")
    print("-" * 50)
    
    try:
        response = requests.post(url, data=test_data, headers=headers, timeout=10)
        print(f"   - Status: {response.status_code}")
        print(f"   - Response: {response.text}")
        
        if response.status_code == 200:
            print("   ✅ Удаленный сервер работает с подписью!")
        else:
            print("   ❌ Удаленный сервер не работает")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    print()
    print("🎉 ТЕСТ ЗАВЕРШЕН!")
    print()
    print("📝 РЕЗУЛЬТАТ:")
    print("   ✅ Проверка webhook без проверки подписи")
    print("   ✅ Тестирование локального и удаленного сервера")
    print("   ✅ Проверка работы с подписью и без подписи")
    print()
    print("⚠️ ВНИМАНИЕ: Проверка подписи отключена для тестирования!")
    print("🔧 После тестирования нужно будет включить проверку подписи обратно")

if __name__ == "__main__":
    test_no_signature()
