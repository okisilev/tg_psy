#!/usr/bin/env python3
"""
Тестовый скрипт для проверки интеграции с Prodamus
"""

import os
import sys
import time
from datetime import datetime, timedelta
from prodamus import ProdаmusAPI
from config import PRODAMUS_DEMO_MODE, SUBSCRIPTION_PRICE

def test_prodamus_connection():
    """Тест подключения к Prodamus API"""
    print("🔗 Тестирование подключения к Prodamus...")
    
    try:
        prodamus = ProdаmusAPI()
        print(f"✅ API инициализирован")
        print(f"   - Shop ID: {prodamus.shop_id}")
        print(f"   - Demo Mode: {prodamus.demo_mode}")
        print(f"   - Secret Key: {'*' * 20}...{prodamus.secret_key[-4:] if prodamus.secret_key else 'Not set'}")
        return True
    except Exception as e:
        print(f"❌ Ошибка инициализации API: {e}")
        return False

def test_payment_creation():
    """Тест создания платежа"""
    print("\n💳 Тестирование создания платежа...")
    
    try:
        prodamus = ProdаmusAPI()
        
        # Тестовые данные
        test_user_id = 12345
        test_username = "test_user"
        
        print(f"   - User ID: {test_user_id}")
        print(f"   - Username: {test_username}")
        print(f"   - Amount: {SUBSCRIPTION_PRICE} копеек")
        print(f"   - Demo Mode: {prodamus.demo_mode}")
        
        # Создаем платеж
        print("   - Отправка запроса к Prodamus API...")
        payment_result = prodamus.create_payment(test_user_id, test_username)
        
        if payment_result:
            print("✅ Платеж успешно создан!")
            print(f"   - Payment ID: {payment_result.get('payment_id')}")
            print(f"   - Payment URL: {payment_result.get('payment_url')}")
            print(f"   - Amount: {payment_result.get('amount')} копеек")
            return payment_result
        else:
            print("❌ Ошибка создания платежа")
            print("   - Возможные причины:")
            print("     • Неверный Shop ID или Secret Key")
            print("     • Проблемы с подключением к API")
            print("     • Неверный формат запроса")
            return None
            
    except Exception as e:
        print(f"❌ Ошибка при создании платежа: {e}")
        return None

def test_payment_status():
    """Тест получения статуса платежа"""
    print("\n📊 Тестирование получения статуса платежа...")
    
    try:
        prodamus = ProdаmusAPI()
        test_order_id = f"test_order_{int(time.time())}"
        
        print(f"   - Order ID: {test_order_id}")
        
        # Получаем статус платежа
        status_result = prodamus.get_payment_status(test_order_id)
        
        if status_result:
            print("✅ Статус платежа получен!")
            print(f"   - Status: {status_result}")
            return status_result
        else:
            print("⚠️ Статус платежа не получен (возможно, заказ не существует)")
            return None
            
    except Exception as e:
        print(f"❌ Ошибка получения статуса платежа: {e}")
        return None

def test_api_methods():
    """Тест дополнительных API методов"""
    print("\n🔧 Тестирование дополнительных API методов...")
    
    try:
        prodamus = ProdаmusAPI()
        test_order_id = f"test_subscription_{int(time.time())}"
        
        # Тест set_activity
        print("   - Тестирование set_activity...")
        activity_result = prodamus.set_activity(test_order_id, "active")
        if activity_result:
            print("   ✅ set_activity: успешно")
        else:
            print("   ⚠️ set_activity: не удалось (возможно, заказ не существует)")
        
        # Тест set_subscription_payment_date
        print("   - Тестирование set_subscription_payment_date...")
        future_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        date_result = prodamus.set_subscription_payment_date(test_order_id, future_date)
        if date_result:
            print(f"   ✅ set_subscription_payment_date: успешно (дата: {future_date})")
        else:
            print("   ⚠️ set_subscription_payment_date: не удалось (возможно, заказ не существует)")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка тестирования API методов: {e}")
        return False

def test_demo_mode():
    """Тест демо-режима"""
    print("\n🧪 Тестирование демо-режима...")
    
    print(f"   - Demo Mode включен: {PRODAMUS_DEMO_MODE}")
    
    if PRODAMUS_DEMO_MODE:
        print("✅ Демо-режим активен - можно использовать тестовые карты:")
        print("   📱 Тестовые карты Сбербанка:")
        print("      МИР: 2202 2050 0001 2424 (05/35, CVC: 669)")
        print("      MasterCard: 5469 9801 0004 8525 (05/26, CVC: 041)")
        print("      Visa: 4006 8009 0096 2514 (05/26, CVC: 941)")
        print("   📱 Другие тестовые карты:")
        print("      Монета: 2200 2400 0000 0006 (12/24, CVC: 123)")
        print("      ГазпромБанк: 4242 4242 4242 4242 (12/30, CVC: 123)")
    else:
        print("⚠️ Демо-режим отключен - будут использоваться реальные платежи!")
    
    return True

def main():
    """Основная функция тестирования"""
    print("🚀 Запуск тестирования интеграции с Prodamus")
    print("=" * 50)
    
    # Проверяем конфигурацию
    if not os.getenv('PRODAMUS_SECRET_KEY'):
        print("❌ PRODAMUS_SECRET_KEY не установлен в переменных окружения")
        print("   Установите переменную или используйте значение по умолчанию из config.py")
    
    # Запускаем тесты
    tests = [
        ("Подключение к API", test_prodamus_connection),
        ("Создание платежа", test_payment_creation),
        ("Статус платежа", test_payment_status),
        ("Дополнительные API", test_api_methods),
        ("Демо-режим", test_demo_mode)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result is not None))
        except Exception as e:
            print(f"❌ Ошибка в тесте '{test_name}': {e}")
            results.append((test_name, False))
    
    # Выводим итоги
    print("\n" + "=" * 50)
    print("📋 ИТОГИ ТЕСТИРОВАНИЯ:")
    
    passed = 0
    for test_name, success in results:
        status = "✅ ПРОЙДЕН" if success else "❌ ПРОВАЛЕН"
        print(f"   {test_name}: {status}")
        if success:
            passed += 1
    
    print(f"\n🎯 Результат: {passed}/{len(results)} тестов пройдено")
    
    if passed == len(results):
        print("🎉 Все тесты пройдены успешно!")
        print("\n📝 Следующие шаги:")
        print("   1. Проверьте webhook URL в настройках Prodamus")
        print("   2. Проведите тестовую оплату с тестовыми картами")
        print("   3. Проверьте получение уведомлений в webhook")
    else:
        print("⚠️ Некоторые тесты не пройдены. Проверьте конфигурацию.")

if __name__ == "__main__":
    main()
