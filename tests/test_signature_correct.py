#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Тест правильной подписи для webhook
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from prodamus import ProdаmusAPI

def test_correct_signature():
    """Тест правильной подписи"""
    
    print("🔐 ТЕСТ ПРАВИЛЬНОЙ ПОДПИСИ")
    print("=" * 50)
    
    # Инициализация
    prodamus = ProdаmusAPI()
    
    # Тестовые данные
    test_data = {
        'order_id': '1',
        'sum': '1000.00',
        'currency': 'rub',
        'payment_status': 'success'
    }
    
    print(f"📋 Тестовые данные:")
    for key, value in test_data.items():
        print(f"   {key}: {value}")
    print()
    
    # Создание подписи
    print(f"🔧 Создание подписи:")
    sign_data = f"{prodamus.shop_id}{test_data['order_id']}{test_data['sum']}{test_data['currency']}{test_data['payment_status']}{prodamus.secret_key}"
    expected_signature = prodamus.generate_signature(sign_data)
    
    print(f"   Данные для подписи: {sign_data}")
    print(f"   Ожидаемая подпись: {expected_signature}")
    print()
    
    # Проверка подписи
    print(f"🧪 Проверка подписи:")
    is_valid = prodamus.verify_webhook(test_data, expected_signature)
    
    if is_valid:
        print("   ✅ Подпись корректна!")
    else:
        print("   ❌ Подпись некорректна!")
    
    print()
    print("📝 Для тестирования webhook используйте:")
    print(f"   curl -X POST https://dashastar.pagekite.me/sales/prodamus \\")
    print(f"     -H 'Sign: {expected_signature}' \\")
    print(f"     -d 'order_id=1&sum=1000.00&currency=rub&payment_status=success'")
    
    return expected_signature

if __name__ == "__main__":
    test_correct_signature()
