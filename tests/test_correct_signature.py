#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Тест с правильной подписью для webhook
"""

import requests
import json
from prodamus import ProdаmusAPI

def test_correct_signature():
    """Тест с правильной подписью"""
    
    print("🧪 ТЕСТ С ПРАВИЛЬНОЙ ПОДПИСЬЮ")
    print("=" * 50)
    
    # Инициализация Prodamus API
    prodamus = ProdаmusAPI()
    
    # Тестовые данные
    test_data = {
        'order_id': '1',
        'sum': '1000.00',
        'currency': 'rub',
        'payment_status': 'success'
    }
    
    # Генерируем правильную подпись
    signature = prodamus.generate_signature(
        f"{prodamus.shop_id}{test_data['order_id']}{test_data['sum']}{test_data['currency']}{test_data['payment_status']}{prodamus.secret_key}"
    )
    
    print(f"📋 Тестовые данные:")
    print(f"   - order_id: {test_data['order_id']}")
    print(f"   - sum: {test_data['sum']}")
    print(f"   - currency: {test_data['currency']}")
    print(f"   - payment_status: {test_data['payment_status']}")
    print(f"   - signature: {signature}")
    print()
    
    # URL для тестирования
    url = "https://dashastar.pagekite.me/sales/prodamus"
    
    # Заголовки
    headers = {
        'Sign': signature
    }
    
    print(f"📋 Тест 1: POST запрос с правильной подписью")
    print("-" * 50)
    
    try:
        response = requests.post(url, data=test_data, headers=headers, timeout=10)
        print(f"   - Status: {response.status_code}")
        print(f"   - Response: {response.text}")
        
        if response.status_code == 200:
            print("   ✅ POST запрос с правильной подписью работает")
        else:
            print("   ❌ POST запрос с правильной подписью не работает")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    print()
    
    # Тест 2: Локальный сервер
    print(f"📋 Тест 2: Локальный сервер")
    print("-" * 50)
    
    try:
        response = requests.post("http://localhost:5000/sales/prodamus", data=test_data, headers=headers, timeout=5)
        print(f"   - Status: {response.status_code}")
        print(f"   - Response: {response.text}")
        
        if response.status_code == 200:
            print("   ✅ Локальный сервер работает")
        else:
            print("   ❌ Локальный сервер не работает")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    print()
    
    # Тест 3: Проверка подписи
    print(f"📋 Тест 3: Проверка подписи")
    print("-" * 50)
    
    # Проверяем подпись
    is_valid = prodamus.verify_webhook(test_data, signature)
    print(f"   - Подпись валидна: {is_valid}")
    
    if is_valid:
        print("   ✅ Подпись корректна")
    else:
        print("   ❌ Подпись некорректна")
    
    print()
    print("🎉 ТЕСТ ЗАВЕРШЕН!")
    print()
    print("📝 РЕЗУЛЬТАТ:")
    print("   ✅ Проверка правильной подписи")
    print("   ✅ Тестирование webhook endpoints")
    print("   ✅ Проверка локального и удаленного сервера")

if __name__ == "__main__":
    test_correct_signature()
