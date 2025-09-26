#!/usr/bin/env python3
"""
Тестовый скрипт для проверки webhook Prodamus
"""

import requests
import json
import hmac
import hashlib
import time
from datetime import datetime

# Конфигурация
WEBHOOK_URL = "http://localhost:5000/webhook/prodamus"  # Замените на ваш URL
SECRET_KEY = "b2f9e8a399225271521dfe88a277a7371cb8c2cebfeaa6f0276ba81fcc303c93"

def generate_signature(data: str) -> str:
    """Генерация подписи для webhook"""
    return hmac.new(
        SECRET_KEY.encode('utf-8'),
        data.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

def test_successful_payment_webhook():
    """Тест webhook для успешного платежа"""
    print("✅ Тестирование webhook успешного платежа...")
    
    # Тестовые данные
    webhook_data = {
        "shop_id": "test_shop",
        "order_id": f"test_success_{int(time.time())}",
        "amount": 1500,
        "currency": "RUB",
        "status": "success",
        "custom_fields": {
            "user_id": "12345",
            "username": "test_user"
        },
        "payment_date": datetime.now().isoformat()
    }
    
    # Создаем подпись
    sign_data = f"{webhook_data['shop_id']}{webhook_data['amount']}{webhook_data['order_id']}{webhook_data['currency']}{webhook_data['status']}{SECRET_KEY}"
    signature = generate_signature(sign_data)
    
    # Отправляем запрос
    headers = {
        'Content-Type': 'application/json',
        'X-Signature': signature
    }
    
    try:
        response = requests.post(WEBHOOK_URL, json=webhook_data, headers=headers, timeout=10)
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Webhook успешно обработан!")
            return True
        else:
            print("❌ Ошибка обработки webhook")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка отправки webhook: {e}")
        return False

def test_failed_payment_webhook():
    """Тест webhook для неудачного платежа"""
    print("\n❌ Тестирование webhook неудачного платежа...")
    
    # Тестовые данные
    webhook_data = {
        "shop_id": "test_shop",
        "order_id": f"test_failed_{int(time.time())}",
        "amount": 1500,
        "currency": "RUB",
        "status": "failed",
        "custom_fields": {
            "user_id": "12346",
            "username": "test_user_failed"
        },
        "payment_date": datetime.now().isoformat()
    }
    
    # Создаем подпись
    sign_data = f"{webhook_data['shop_id']}{webhook_data['amount']}{webhook_data['order_id']}{webhook_data['currency']}{webhook_data['status']}{SECRET_KEY}"
    signature = generate_signature(sign_data)
    
    # Отправляем запрос
    headers = {
        'Content-Type': 'application/json',
        'X-Signature': signature
    }
    
    try:
        response = requests.post(WEBHOOK_URL, json=webhook_data, headers=headers, timeout=10)
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Webhook успешно обработан!")
            return True
        else:
            print("❌ Ошибка обработки webhook")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка отправки webhook: {e}")
        return False

def test_invalid_signature():
    """Тест webhook с неверной подписью"""
    print("\n🔒 Тестирование webhook с неверной подписью...")
    
    # Тестовые данные
    webhook_data = {
        "shop_id": "test_shop",
        "order_id": f"test_invalid_{int(time.time())}",
        "amount": 1500,
        "currency": "RUB",
        "status": "success",
        "custom_fields": {
            "user_id": "12347",
            "username": "test_user_invalid"
        }
    }
    
    # Неверная подпись
    signature = "invalid_signature"
    
    # Отправляем запрос
    headers = {
        'Content-Type': 'application/json',
        'X-Signature': signature
    }
    
    try:
        response = requests.post(WEBHOOK_URL, json=webhook_data, headers=headers, timeout=10)
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 400:
            print("✅ Webhook правильно отклонил неверную подпись!")
            return True
        else:
            print("❌ Webhook не отклонил неверную подпись")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка отправки webhook: {e}")
        return False

def test_health_check():
    """Тест проверки здоровья сервиса"""
    print("\n🏥 Тестирование health check...")
    
    try:
        health_url = WEBHOOK_URL.replace('/webhook/prodamus', '/health')
        response = requests.get(health_url, timeout=10)
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Health check прошел успешно!")
            return True
        else:
            print("❌ Health check не прошел")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка health check: {e}")
        return False

def main():
    """Основная функция тестирования webhook"""
    print("🚀 Запуск тестирования webhook Prodamus")
    print("=" * 50)
    print(f"Webhook URL: {WEBHOOK_URL}")
    print(f"Secret Key: {'*' * 20}...{SECRET_KEY[-4:]}")
    print()
    
    # Запускаем тесты
    tests = [
        ("Health Check", test_health_check),
        ("Успешный платеж", test_successful_payment_webhook),
        ("Неудачный платеж", test_failed_payment_webhook),
        ("Неверная подпись", test_invalid_signature)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Ошибка в тесте '{test_name}': {e}")
            results.append((test_name, False))
    
    # Выводим итоги
    print("\n" + "=" * 50)
    print("📋 ИТОГИ ТЕСТИРОВАНИЯ WEBHOOK:")
    
    passed = 0
    for test_name, success in results:
        status = "✅ ПРОЙДЕН" if success else "❌ ПРОВАЛЕН"
        print(f"   {test_name}: {status}")
        if success:
            passed += 1
    
    print(f"\n🎯 Результат: {passed}/{len(results)} тестов пройдено")
    
    if passed == len(results):
        print("🎉 Все тесты webhook пройдены успешно!")
    else:
        print("⚠️ Некоторые тесты webhook не пройдены.")
        print("\n📝 Возможные причины:")
        print("   1. Webhook сервер не запущен")
        print("   2. Неверный URL webhook")
        print("   3. Проблемы с конфигурацией")

if __name__ == "__main__":
    main()
