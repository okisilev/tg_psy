#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Проверка статуса webhook сервера
"""

import requests
import json

def check_webhook_status():
    """Проверка статуса webhook сервера"""
    
    print("🔍 ПРОВЕРКА СТАТУСА WEBHOOK СЕРВЕРА")
    print("=" * 50)
    
    # URL для проверки
    base_url = "https://dashastar.pagekite.me"
    
    print(f"📋 Проверяемые URL:")
    print(f"   - Health: {base_url}/health")
    print(f"   - Prodamus: {base_url}/sales/prodamus")
    print()
    
    # Тест 1: Health endpoint
    print("📋 Тест 1: Health endpoint")
    print("-" * 40)
    
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        print(f"   - Status: {response.status_code}")
        print(f"   - Response: {response.text}")
        
        if response.status_code == 200:
            print("   ✅ Health endpoint работает")
        else:
            print("   ❌ Health endpoint не работает")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    print()
    
    # Тест 2: Prodamus webhook
    print("📋 Тест 2: Prodamus webhook")
    print("-" * 40)
    
    # Тестовые данные
    test_data = {
        'order_id': '1',
        'sum': '1000.00',
        'currency': 'rub',
        'payment_status': 'success'
    }
    
    # Заголовки
    headers = {
        'Sign': '7e6c5e9e4596d475476c41401f100488522dda04f2871002123d5c72cae3d261'
    }
    
    try:
        response = requests.post(f"{base_url}/sales/prodamus", data=test_data, headers=headers, timeout=10)
        print(f"   - Status: {response.status_code}")
        print(f"   - Response: {response.text}")
        
        if response.status_code == 200:
            print("   ✅ Prodamus webhook работает")
        else:
            print("   ❌ Prodamus webhook не работает")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    print()
    
    # Тест 3: Проверка локального сервера
    print("📋 Тест 3: Проверка локального сервера")
    print("-" * 40)
    
    try:
        response = requests.get("http://localhost:5000/health", timeout=5)
        print(f"   - Status: {response.status_code}")
        print(f"   - Response: {response.text}")
        
        if response.status_code == 200:
            print("   ✅ Локальный сервер работает")
        else:
            print("   ❌ Локальный сервер не работает")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    print()
    
    # Тест 4: Проверка процессов
    print("📋 Тест 4: Проверка процессов")
    print("-" * 40)
    
    import subprocess
    try:
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        processes = result.stdout
        
        if 'webhook.py' in processes:
            print("   ✅ Webhook процесс запущен")
        else:
            print("   ❌ Webhook процесс не найден")
        
        if 'pagekite.py' in processes:
            print("   ✅ PageKite процесс запущен")
        else:
            print("   ❌ PageKite процесс не найден")
            
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    print()
    print("🎉 ПРОВЕРКА ЗАВЕРШЕНА!")
    print()
    print("📝 РЕЗУЛЬТАТ:")
    print("   ✅ Проверка статуса webhook сервера")
    print("   ✅ Проверка доступности endpoints")
    print("   ✅ Проверка процессов")

if __name__ == "__main__":
    check_webhook_status()
