#!/usr/bin/env python3
"""
Тест проверки подписи webhook от Prodamus
"""

import hashlib
import hmac
from prodamus import ProdаmusAPI

def test_signature():
    """Тест проверки подписи"""
    print("🔐 ТЕСТ ПРОВЕРКИ ПОДПИСИ WEBHOOK")
    print("=" * 50)
    
    # Создаем экземпляр API
    prodamus = ProdаmusAPI()
    
    # Тестовые данные от Prodamus
    test_data = {
        'order_id': 'women_club_431292182_test',
        'sum': '50.00',
        'currency': 'rub',
        'payment_status': 'success'
    }
    
    print("📋 Тестовые данные:")
    for key, value in test_data.items():
        print(f"   {key}: {value}")
    print()
    
    # Создаем правильную подпись используя метод API
    sign_data = f"{prodamus.shop_id}{test_data['order_id']}{test_data['sum']}{test_data['currency']}{test_data['payment_status']}{prodamus.secret_key}"
    correct_signature = prodamus.generate_signature(sign_data)
    
    print("🔧 Создание подписи:")
    print(f"   Данные для подписи: {sign_data}")
    print(f"   Правильная подпись: {correct_signature}")
    print()
    
    # Тестируем проверку подписи
    print("🧪 Тест проверки подписи:")
    
    # Тест 1: Правильная подпись
    result1 = prodamus.verify_webhook(test_data, correct_signature)
    print(f"   ✅ Правильная подпись: {'ПРОЙДЕН' if result1 else 'ПРОВАЛЕН'}")
    
    # Тест 2: Неправильная подпись
    wrong_signature = "wrong_signature"
    result2 = prodamus.verify_webhook(test_data, wrong_signature)
    print(f"   ❌ Неправильная подпись: {'ПРОВАЛЕН' if not result2 else 'ПРОЙДЕН'}")
    
    # Тест 3: Пустая подпись
    result3 = prodamus.verify_webhook(test_data, "")
    print(f"   ⚠️ Пустая подпись: {'ПРОВАЛЕН' if not result3 else 'ПРОЙДЕН'}")
    
    print()
    print("📝 Результат:")
    if result1 and not result2 and not result3:
        print("   ✅ Проверка подписи работает корректно!")
    else:
        print("   ❌ Проверка подписи работает некорректно!")
    
    print()
    print("🔗 Для тестирования webhook используйте:")
    print(f"   curl -X POST http://localhost:5001/sales/prodamus \\")
    print(f"     -H 'Content-Type: application/json' \\")
    print(f"     -H 'Sign: {correct_signature}' \\")
    print(f"     -d '{test_data}'")

if __name__ == "__main__":
    test_signature()
