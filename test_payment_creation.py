#!/usr/bin/env python3
"""
Тест создания платежа с исправленным методом
"""

import os
import sys
from datetime import datetime

def test_payment_creation():
    """Тест создания платежа"""
    print("💳 Тестирование создания платежа...")
    print("=" * 50)
    
    try:
        from prodamus import ProdаmusAPI
        
        # Создаем экземпляр API
        api = ProdаmusAPI()
        
        # Тестовые данные
        test_user_id = 431292182
        test_username = "Fun_Oleg"
        
        print(f"🔧 Параметры:")
        print(f"   - User ID: {test_user_id}")
        print(f"   - Username: {test_username}")
        print(f"   - Shop ID: {api.shop_id}")
        print(f"   - Demo Mode: {api.demo_mode}")
        print()
        
        # Создаем платеж
        print("🚀 Создание платежа...")
        payment_result = api.create_payment(test_user_id, test_username)
        
        if payment_result:
            print("✅ Платеж создан успешно!")
            print(f"   - Payment ID: {payment_result.get('payment_id')}")
            print(f"   - Amount: {payment_result.get('amount')} копеек")
            print(f"   - Payment URL: {payment_result.get('payment_url')}")
            print()
            
            # Проверяем URL
            payment_url = payment_result.get('payment_url')
            if payment_url and 'dashastar.payform.ru' in payment_url:
                print("✅ URL платежа корректен")
                print("📝 Теперь можно:")
                print("   1. Открыть URL в браузере")
                print("   2. Использовать тестовые карты для оплаты")
                print("   3. Проверить получение webhook уведомлений")
                return True
            else:
                print("❌ URL платежа некорректен")
                return False
        else:
            print("❌ Ошибка создания платежа")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def test_demo_cards():
    """Тест демо-карт"""
    print("\n🧪 Тестовые карты для демо-режима:")
    print("-" * 50)
    
    demo_cards = [
        {"name": "МИР", "number": "2202 2050 0001 2424", "expiry": "05/35", "cvc": "669"},
        {"name": "MasterCard", "number": "5469 9801 0004 8525", "expiry": "05/26", "cvc": "041"},
        {"name": "Visa", "number": "4006 8009 0096 2514", "expiry": "05/26", "cvc": "941"},
        {"name": "Монета", "number": "2200 2400 0000 0006", "expiry": "12/24", "cvc": "123"},
        {"name": "ГазпромБанк", "number": "4242 4242 4242 4242", "expiry": "12/30", "cvc": "123"}
    ]
    
    for card in demo_cards:
        print(f"📱 {card['name']}: {card['number']} ({card['expiry']}, CVC: {card['cvc']})")
    
    return True

def main():
    """Основная функция"""
    print("🚀 ТЕСТ СОЗДАНИЯ ПЛАТЕЖА PRODAMUS")
    print("=" * 60)
    print(f"Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Тестируем создание платежа
    payment_success = test_payment_creation()
    
    # Показываем демо-карты
    demo_success = test_demo_cards()
    
    # Итоги
    print("\n" + "=" * 60)
    print("📋 ИТОГИ ТЕСТИРОВАНИЯ:")
    
    if payment_success:
        print("✅ Создание платежа: ПРОЙДЕН")
    else:
        print("❌ Создание платежа: ПРОВАЛЕН")
    
    if demo_success:
        print("✅ Демо-карты: ПРОЙДЕН")
    else:
        print("❌ Демо-карты: ПРОВАЛЕН")
    
    if payment_success and demo_success:
        print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
        print("\n📝 Следующие шаги:")
        print("   1. Запустите webhook сервер: python3 start_webhook.py")
        print("   2. Откройте URL платежа в браузере")
        print("   3. Используйте тестовые карты для оплаты")
        print("   4. Проверьте получение webhook уведомлений")
    else:
        print("\n⚠️ Некоторые тесты не пройдены")
        print("📝 Проверьте конфигурацию и попробуйте снова")

if __name__ == "__main__":
    main()
