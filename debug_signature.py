#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Отладка подписи для webhook
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from prodamus import ProdаmusAPI

def debug_signature():
    """Отладка подписи"""
    
    print("🔐 ОТЛАДКА ПОДПИСИ")
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
    
    print(f"   Shop ID: {prodamus.shop_id}")
    print(f"   Secret Key: {prodamus.secret_key[:10]}...")
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
    
    # Тест с разными данными
    print(f"🧪 Тест с разными данными:")
    
    # Тест 1: Точные данные от Prodamus
    prodamus_data = {
        'order_id': '1',
        'sum': '1000.00',
        'currency': 'rub',
        'payment_status': 'success'
    }
    
    sign_data_prodamus = f"{prodamus.shop_id}{prodamus_data['order_id']}{prodamus_data['sum']}{prodamus_data['currency']}{prodamus_data['payment_status']}{prodamus.secret_key}"
    signature_prodamus = prodamus.generate_signature(sign_data_prodamus)
    
    print(f"   Данные Prodamus: {sign_data_prodamus}")
    print(f"   Подпись Prodamus: {signature_prodamus}")
    
    # Проверка
    is_valid_prodamus = prodamus.verify_webhook(prodamus_data, signature_prodamus)
    print(f"   Результат: {'✅ Корректна' if is_valid_prodamus else '❌ Некорректна'}")
    
    print()
    print("📝 Для тестирования webhook используйте:")
    print(f"   curl -X POST https://dashastar.pagekite.me/sales/prodamus \\")
    print(f"     -H 'Sign: {signature_prodamus}' \\")
    print(f"     -d 'order_id=1&sum=1000.00&currency=rub&payment_status=success'")
    
    return signature_prodamus

if __name__ == "__main__":
    debug_signature()
