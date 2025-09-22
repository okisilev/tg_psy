#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Поиск правильного алгоритма подписи Prodamus
"""

import hashlib
import hmac
import json
from typing import Dict, Any

def find_signature_algorithm():
    """Поиск правильного алгоритма подписи"""
    
    print("🔍 ПОИСК ПРАВИЛЬНОГО АЛГОРИТМА ПОДПИСИ")
    print("=" * 50)
    
    # Тестовые данные от Prodamus
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
    print(f"   - Полученная подпись: {received_signature}")
    print()
    
    # Список алгоритмов для проверки
    algorithms = [
        # Алгоритм 1: Простая конкатенация всех значений
        {
            'name': 'Простая конкатенация всех значений',
            'func': lambda data, key: _simple_concat(data, key)
        },
        
        # Алгоритм 2: С сортировкой ключей
        {
            'name': 'С сортировкой ключей',
            'func': lambda data, key: _sorted_concat(data, key)
        },
        
        # Алгоритм 3: Только основные поля
        {
            'name': 'Только основные поля',
            'func': lambda data, key: _main_fields(data, key)
        },
        
        # Алгоритм 4: Без секретного ключа
        {
            'name': 'Без секретного ключа',
            'func': lambda data, key: _no_secret(data, key)
        },
        
        # Алгоритм 5: Секретный ключ в начале
        {
            'name': 'Секретный ключ в начале',
            'func': lambda data, key: _secret_first(data, key)
        },
        
        # Алгоритм 6: Только order_id + sum + payment_status
        {
            'name': 'Только order_id + sum + payment_status',
            'func': lambda data, key: _minimal_fields(data, key)
        },
        
        # Алгоритм 7: JSON сериализация
        {
            'name': 'JSON сериализация',
            'func': lambda data, key: _json_serialization(data, key)
        },
        
        # Алгоритм 8: MD5 хеш
        {
            'name': 'MD5 хеш',
            'func': lambda data, key: _md5_hash(data, key)
        },
        
        # Алгоритм 9: SHA1 хеш
        {
            'name': 'SHA1 хеш',
            'func': lambda data, key: _sha1_hash(data, key)
        },
        
        # Алгоритм 10: SHA256 без HMAC
        {
            'name': 'SHA256 без HMAC',
            'func': lambda data, key: _sha256_no_hmac(data, key)
        },
        
        # Алгоритм 11: Только order_id + secret_key
        {
            'name': 'Только order_id + secret_key',
            'func': lambda data, key: _order_id_only(data, key)
        },
        
        # Алгоритм 12: Только sum + secret_key
        {
            'name': 'Только sum + secret_key',
            'func': lambda data, key: _sum_only(data, key)
        },
        
        # Алгоритм 13: Только payment_status + secret_key
        {
            'name': 'Только payment_status + secret_key',
            'func': lambda data, key: _payment_status_only(data, key)
        },
        
        # Алгоритм 14: order_id + sum + secret_key
        {
            'name': 'order_id + sum + secret_key',
            'func': lambda data, key: _order_id_sum(data, key)
        },
        
        # Алгоритм 15: sum + payment_status + secret_key
        {
            'name': 'sum + payment_status + secret_key',
            'func': lambda data, key: _sum_payment_status(data, key)
        }
    ]
    
    print("🔍 Проверка алгоритмов:")
    print("-" * 50)
    
    found_match = False
    
    for i, algorithm in enumerate(algorithms, 1):
        try:
            signature = algorithm['func'](test_data, secret_key)
            print(f"   Алгоритм {i}: {algorithm['name']}")
            print(f"   Подпись: {signature}")
            
            if signature == received_signature:
                print(f"   ✅ НАЙДЕН ПРАВИЛЬНЫЙ АЛГОРИТМ: {algorithm['name']}")
                found_match = True
                break
            else:
                print(f"   ❌ Не совпадает")
            
            print()
            
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")
            print()
    
    if not found_match:
        print("❌ Правильный алгоритм не найден")
        print("🔧 Рекомендации:")
        print("   1. Обратиться в поддержку Prodamus")
        print("   2. Изучить исходный код PHP библиотеки Hmac")
        print("   3. Проанализировать другие поля данных")
        print("   4. Попробовать другие комбинации полей")
    else:
        print("🎉 ПРАВИЛЬНЫЙ АЛГОРИТМ НАЙДЕН!")
        print("🔧 Теперь можно включить проверку подписи обратно")

def _simple_concat(data: Dict[str, Any], secret_key: str) -> str:
    """Простая конкатенация всех значений"""
    sign_string = ""
    for key, value in data.items():
        if key not in ['signature', 'sign']:
            sign_string += str(value)
    sign_string += secret_key
    
    return hmac.new(
        secret_key.encode('utf-8'),
        sign_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

def _sorted_concat(data: Dict[str, Any], secret_key: str) -> str:
    """С сортировкой ключей"""
    sorted_keys = sorted(data.keys())
    sign_string = ""
    for key in sorted_keys:
        if key not in ['signature', 'sign']:
            sign_string += str(data[key])
    sign_string += secret_key
    
    return hmac.new(
        secret_key.encode('utf-8'),
        sign_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

def _main_fields(data: Dict[str, Any], secret_key: str) -> str:
    """Только основные поля"""
    main_fields = ['order_id', 'sum', 'payment_status', 'customer_email']
    sign_string = ""
    for field in main_fields:
        if field in data:
            sign_string += str(data[field])
    sign_string += secret_key
    
    return hmac.new(
        secret_key.encode('utf-8'),
        sign_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

def _no_secret(data: Dict[str, Any], secret_key: str) -> str:
    """Без секретного ключа"""
    sign_string = ""
    for key, value in data.items():
        if key not in ['signature', 'sign']:
            sign_string += str(value)
    
    return hmac.new(
        secret_key.encode('utf-8'),
        sign_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

def _secret_first(data: Dict[str, Any], secret_key: str) -> str:
    """Секретный ключ в начале"""
    sign_string = secret_key
    for key, value in data.items():
        if key not in ['signature', 'sign']:
            sign_string += str(value)
    
    return hmac.new(
        secret_key.encode('utf-8'),
        sign_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

def _minimal_fields(data: Dict[str, Any], secret_key: str) -> str:
    """Только order_id + sum + payment_status"""
    sign_string = f"{data.get('order_id', '')}{data.get('sum', '')}{data.get('payment_status', '')}{secret_key}"
    
    return hmac.new(
        secret_key.encode('utf-8'),
        sign_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

def _json_serialization(data: Dict[str, Any], secret_key: str) -> str:
    """JSON сериализация"""
    json_data = json.dumps(data, sort_keys=True, separators=(',', ':'))
    sign_string = json_data + secret_key
    
    return hmac.new(
        secret_key.encode('utf-8'),
        sign_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

def _md5_hash(data: Dict[str, Any], secret_key: str) -> str:
    """MD5 хеш"""
    sign_string = ""
    for key, value in data.items():
        if key not in ['signature', 'sign']:
            sign_string += str(value)
    sign_string += secret_key
    
    return hmac.new(
        secret_key.encode('utf-8'),
        sign_string.encode('utf-8'),
        hashlib.md5
    ).hexdigest()

def _sha1_hash(data: Dict[str, Any], secret_key: str) -> str:
    """SHA1 хеш"""
    sign_string = ""
    for key, value in data.items():
        if key not in ['signature', 'sign']:
            sign_string += str(value)
    sign_string += secret_key
    
    return hmac.new(
        secret_key.encode('utf-8'),
        sign_string.encode('utf-8'),
        hashlib.sha1
    ).hexdigest()

def _sha256_no_hmac(data: Dict[str, Any], secret_key: str) -> str:
    """SHA256 без HMAC"""
    sign_string = ""
    for key, value in data.items():
        if key not in ['signature', 'sign']:
            sign_string += str(value)
    sign_string += secret_key
    
    return hashlib.sha256(sign_string.encode('utf-8')).hexdigest()

def _order_id_only(data: Dict[str, Any], secret_key: str) -> str:
    """Только order_id + secret_key"""
    sign_string = f"{data.get('order_id', '')}{secret_key}"
    
    return hmac.new(
        secret_key.encode('utf-8'),
        sign_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

def _sum_only(data: Dict[str, Any], secret_key: str) -> str:
    """Только sum + secret_key"""
    sign_string = f"{data.get('sum', '')}{secret_key}"
    
    return hmac.new(
        secret_key.encode('utf-8'),
        sign_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

def _payment_status_only(data: Dict[str, Any], secret_key: str) -> str:
    """Только payment_status + secret_key"""
    sign_string = f"{data.get('payment_status', '')}{secret_key}"
    
    return hmac.new(
        secret_key.encode('utf-8'),
        sign_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

def _order_id_sum(data: Dict[str, Any], secret_key: str) -> str:
    """order_id + sum + secret_key"""
    sign_string = f"{data.get('order_id', '')}{data.get('sum', '')}{secret_key}"
    
    return hmac.new(
        secret_key.encode('utf-8'),
        sign_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

def _sum_payment_status(data: Dict[str, Any], secret_key: str) -> str:
    """sum + payment_status + secret_key"""
    sign_string = f"{data.get('sum', '')}{data.get('payment_status', '')}{secret_key}"
    
    return hmac.new(
        secret_key.encode('utf-8'),
        sign_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

if __name__ == "__main__":
    find_signature_algorithm()
