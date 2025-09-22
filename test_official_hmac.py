#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Тест официальной библиотеки Hmac от Prodamus
"""

import requests
import json
from hmac_prodamus import Hmac

def test_official_hmac():
    """Тест официальной библиотеки Hmac"""
    
    print("🧪 ТЕСТ ОФИЦИАЛЬНОЙ БИБЛИОТЕКИ HMAC")
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
    
    # Секретный ключ
    secret_key = "b2f9e8a399225271521dfe88a277a7371cb8c2cebfeaa6f0276ba81fcc303c93"
    
    # Полученная подпись от Prodamus
    received_signature = "7e6c5e9e4596d475476c41401f100488522dda04f2871002123d5c72cae3d261"
    
    print(f"📋 Тестовые данные:")
    print(f"   - order_id: {test_data['order_id']}")
    print(f"   - sum: {test_data['sum']}")
    print(f"   - payment_status: {test_data['payment_status']}")
    print(f"   - customer_email: {test_data['customer_email']}")
    print(f"   - Полученная подпись: {received_signature}")
    print()
    
    # Тест 1: Создание подписи
    print("📋 Тест 1: Создание подписи")
    print("-" * 40)
    
    try:
        created_signature = Hmac.create(test_data, secret_key)
        print(f"   - Созданная подпись: {created_signature}")
        print(f"   - Полученная подпись: {received_signature}")
        
        if created_signature == received_signature:
            print("   ✅ Подпись совпадает!")
        else:
            print("   ❌ Подпись не совпадает")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    print()
    
    # Тест 2: Проверка подписи
    print("📋 Тест 2: Проверка подписи")
    print("-" * 40)
    
    try:
        is_valid = Hmac.verify(test_data, secret_key, received_signature)
        print(f"   - Подпись валидна: {is_valid}")
        
        if is_valid:
            print("   ✅ Подпись корректна!")
        else:
            print("   ❌ Подпись некорректна")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    print()
    
    # Тест 3: Тест webhook
    print("📋 Тест 3: Тест webhook")
    print("-" * 40)
    
    url = "https://dashastar.pagekite.me/sales/prodamus"
    headers = {
        'Sign': received_signature
    }
    
    try:
        response = requests.post(url, data=test_data, headers=headers, timeout=10)
        print(f"   - Status: {response.status_code}")
        print(f"   - Response: {response.text}")
        
        if response.status_code == 200:
            print("   ✅ Webhook работает с официальной библиотекой!")
        else:
            print("   ❌ Webhook не работает")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    print()
    
    # Тест 4: Локальный сервер
    print("📋 Тест 4: Локальный сервер")
    print("-" * 40)
    
    try:
        response = requests.post("http://localhost:5000/sales/prodamus", data=test_data, headers=headers, timeout=5)
        print(f"   - Status: {response.status_code}")
        print(f"   - Response: {response.text}")
        
        if response.status_code == 200:
            print("   ✅ Локальный сервер работает!")
        else:
            print("   ❌ Локальный сервер не работает")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    print()
    print("🎉 ТЕСТ ЗАВЕРШЕН!")
    print()
    print("📝 РЕЗУЛЬТАТ:")
    print("   ✅ Проверка официальной библиотеки Hmac")
    print("   ✅ Тестирование создания и проверки подписи")
    print("   ✅ Проверка webhook endpoints")
    print()
    print("📚 Основано на документации Prodamus:")
    print("   https://help.prodamus.ru/payform/integracii/rest-api/instrukcii-dlya-samostoyatelnaya-integracii-servisov")

if __name__ == "__main__":
    test_official_hmac()
