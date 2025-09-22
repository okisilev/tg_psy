#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Тест POST запросов к webhook
"""

import requests
import json

def test_post_webhook():
    """Тест POST запросов к webhook"""
    
    print("🧪 ТЕСТ POST ЗАПРОСОВ К WEBHOOK")
    print("=" * 50)
    
    # URL для тестирования
    url = "https://dashastar.pagekite.me/sales/prodamus"
    
    print(f"📋 Тестовые данные:")
    print(f"   - URL: {url}")
    print()
    
    # Тест 1: Простой POST запрос
    print("📋 Тест 1: Простой POST запрос")
    print("-" * 40)
    
    try:
        response = requests.post(url, data={'test': 'data'}, timeout=10)
        print(f"   - Status: {response.status_code}")
        print(f"   - Response: {response.text}")
        
        if response.status_code == 200:
            print("   ✅ POST запрос работает")
        else:
            print("   ❌ POST запрос не работает")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    print()
    
    # Тест 2: POST с заголовками
    print("📋 Тест 2: POST с заголовками")
    print("-" * 40)
    
    headers = {
        'Sign': '7e6c5e9e4596d475476c41401f100488522dda04f2871002123d5c72cae3d261'
    }
    
    data = {
        'order_id': '1',
        'sum': '1000.00',
        'currency': 'rub',
        'payment_status': 'success'
    }
    
    try:
        response = requests.post(url, data=data, headers=headers, timeout=10)
        print(f"   - Status: {response.status_code}")
        print(f"   - Response: {response.text}")
        
        if response.status_code == 200:
            print("   ✅ POST с заголовками работает")
        else:
            print("   ❌ POST с заголовками не работает")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    print()
    
    # Тест 3: POST с JSON
    print("📋 Тест 3: POST с JSON")
    print("-" * 40)
    
    json_data = {
        'order_id': '1',
        'sum': '1000.00',
        'currency': 'rub',
        'payment_status': 'success'
    }
    
    json_headers = {
        'Content-Type': 'application/json',
        'Sign': '7e6c5e9e4596d475476c41401f100488522dda04f2871002123d5c72cae3d261'
    }
    
    try:
        response = requests.post(url, json=json_data, headers=json_headers, timeout=10)
        print(f"   - Status: {response.status_code}")
        print(f"   - Response: {response.text}")
        
        if response.status_code == 200:
            print("   ✅ POST с JSON работает")
        else:
            print("   ❌ POST с JSON не работает")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    print()
    
    # Тест 4: Проверка локального сервера
    print("📋 Тест 4: Проверка локального сервера")
    print("-" * 40)
    
    try:
        response = requests.post("http://localhost:5000/sales/prodamus", data=data, headers=headers, timeout=5)
        print(f"   - Status: {response.status_code}")
        print(f"   - Response: {response.text}")
        
        if response.status_code == 200:
            print("   ✅ Локальный сервер работает")
        else:
            print("   ❌ Локальный сервер не работает")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    print()
    print("🎉 ТЕСТ ЗАВЕРШЕН!")
    print()
    print("📝 РЕЗУЛЬТАТ:")
    print("   ✅ Проверка POST запросов к webhook")
    print("   ✅ Проверка работы с разными форматами данных")
    print("   ✅ Проверка локального и удаленного сервера")

if __name__ == "__main__":
    test_post_webhook()
