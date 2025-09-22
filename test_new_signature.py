#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Тест подписи для нового запроса от Prodamus
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from prodamus import ProdаmusAPI

def test_new_signature():
    """Тест подписи для нового запроса"""
    
    print("🔐 ТЕСТ ПОДПИСИ ДЛЯ НОВОГО ЗАПРОСА")
    print("=" * 50)
    
    # Данные из нового запроса
    test_data = {
        'order_id': '35994004',
        'sum': '50.00',
        'currency': 'rub',
        'payment_status': 'success'
    }
    
    # Полученная подпись от Prodamus
    received_signature = "30ba444dc24a268bdb78669632c6e0777652c0e63217b6cbc9adcb5fb2a0adaa"
    
    print(f"📋 Данные запроса:")
    for key, value in test_data.items():
        print(f"   {key}: {value}")
    
    print(f"\n🔧 Создание подписи:")
    
    # Создаем API объект
    api = ProdаmusAPI()
    
    # Создаем строку для подписи
    sign_data = f"{api.shop_id}{test_data['order_id']}{test_data['sum']}{test_data['currency']}{test_data['payment_status']}{api.secret_key}"
    expected_signature = api.generate_signature(sign_data)
    
    print(f"   Данные для подписи: {sign_data}")
    print(f"   Полученная подпись: {received_signature}")
    print(f"   Ожидаемая подпись: {expected_signature}")
    
    # Проверяем подпись
    is_valid = api.verify_webhook(test_data, received_signature)
    
    print(f"\n🧪 Результат проверки:")
    if is_valid:
        print("   ✅ Подпись корректна!")
    else:
        print("   ❌ Подпись неверна!")
    
    print(f"\n🔗 Тест webhook:")
    print(f"   curl -X POST http://82.147.71.244:5000/sales/prodamus \\")
    print(f"     -H 'Content-Type: application/json' \\")
    print(f"     -H 'Sign: {received_signature}' \\")
    print(f"     -d '{test_data}'")
    
    return is_valid

if __name__ == "__main__":
    test_new_signature()
