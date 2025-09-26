#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Тест подписи от Prodamus
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from prodamus import ProdаmusAPI

def test_prodamus_signature():
    """Тест подписи от Prodamus"""
    
    print("🔐 ТЕСТ ПОДПИСИ ОТ PRODAMUS")
    print("=" * 50)
    
    # Инициализация
    prodamus = ProdаmusAPI()
    
    # Данные от Prodamus
    prodamus_data = {
        'order_id': '1',
        'sum': '1000.00',
        'currency': 'rub',
        'payment_status': 'success'
    }
    
    # Подпись от Prodamus
    prodamus_signature = "7e6c5e9e4596d475476c41401f100488522dda04f2871002123d5c72cae3d261"
    
    print(f"📋 Данные от Prodamus:")
    for key, value in prodamus_data.items():
        print(f"   {key}: {value}")
    print(f"   Подпись от Prodamus: {prodamus_signature}")
    print()
    
    # Тест 1: Стандартный формат
    print("📋 Тест 1: Стандартный формат")
    print("-" * 40)
    
    sign_data_standard = f"{prodamus.shop_id}{prodamus_data['order_id']}{prodamus_data['sum']}{prodamus_data['currency']}{prodamus_data['payment_status']}{prodamus.secret_key}"
    standard_signature = prodamus.generate_signature(sign_data_standard)
    
    print(f"   Данные: {sign_data_standard}")
    print(f"   Подпись: {standard_signature}")
    
    if prodamus_signature == standard_signature:
        print("   ✅ Подпись совпадает со стандартным форматом")
    else:
        print("   ❌ Подпись не совпадает со стандартным форматом")
    
    print()
    
    # Тест 2: Альтернативный формат
    print("📋 Тест 2: Альтернативный формат")
    print("-" * 40)
    
    sign_data_alt = f"{prodamus_data['order_id']}{prodamus_data['sum']}{prodamus_data['currency']}{prodamus_data['payment_status']}{prodamus.secret_key}"
    alt_signature = prodamus.generate_signature(sign_data_alt)
    
    print(f"   Данные: {sign_data_alt}")
    print(f"   Подпись: {alt_signature}")
    
    if prodamus_signature == alt_signature:
        print("   ✅ Подпись совпадает с альтернативным форматом")
    else:
        print("   ❌ Подпись не совпадает с альтернативным форматом")
    
    print()
    
    # Тест 3: Проверка через verify_webhook
    print("📋 Тест 3: Проверка через verify_webhook")
    print("-" * 40)
    
    is_valid = prodamus.verify_webhook(prodamus_data, prodamus_signature)
    
    if is_valid:
        print("   ✅ Подпись валидна")
    else:
        print("   ❌ Подпись невалидна")
    
    print()
    
    # Тест 4: Разные варианты данных
    print("📋 Тест 4: Разные варианты данных")
    print("-" * 40)
    
    # Вариант 1: Без shop_id
    sign_data_no_shop = f"{prodamus_data['order_id']}{prodamus_data['sum']}{prodamus_data['currency']}{prodamus_data['payment_status']}{prodamus.secret_key}"
    signature_no_shop = prodamus.generate_signature(sign_data_no_shop)
    print(f"   Без shop_id: {signature_no_shop}")
    
    # Вариант 2: Только основные поля
    sign_data_basic = f"{prodamus_data['order_id']}{prodamus_data['sum']}{prodamus_data['payment_status']}{prodamus.secret_key}"
    signature_basic = prodamus.generate_signature(sign_data_basic)
    print(f"   Только основные: {signature_basic}")
    
    # Вариант 3: С дополнительными полями
    sign_data_extra = f"{prodamus_data['order_id']}{prodamus_data['sum']}{prodamus_data['currency']}{prodamus_data['payment_status']}{prodamus.secret_key}"
    signature_extra = prodamus.generate_signature(sign_data_extra)
    print(f"   С дополнительными: {signature_extra}")
    
    print()
    print("🎉 ТЕСТ ЗАВЕРШЕН!")
    print()
    print("📝 РЕЗУЛЬТАТ:")
    if is_valid:
        print("   ✅ Подпись от Prodamus валидна")
        print("   ✅ Webhook будет принимать данные от Prodamus")
    else:
        print("   ❌ Подпись от Prodamus невалидна")
        print("   ❌ Нужно проверить алгоритм генерации подписи")

if __name__ == "__main__":
    test_prodamus_signature()
