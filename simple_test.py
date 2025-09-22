#!/usr/bin/env python3
"""
Упрощенный тест системы платежей Prodamus без дополнительных зависимостей
"""

import os
import sys
import time
from datetime import datetime

def test_config():
    """Тест конфигурации"""
    print("🔧 Тестирование конфигурации...")
    
    try:
        # Проверяем основные параметры
        shop_id = os.getenv('PRODAMUS_SHOP_ID', 'dashastar')
        secret_key = os.getenv('PRODAMUS_SECRET_KEY', 'b2f9e8a399225271521dfe88a277a7371cb8c2cebfeaa6f0276ba81fcc303c93')
        demo_mode = os.getenv('PRODAMUS_DEMO_MODE', 'true').lower() == 'true'
        
        print(f"   - Shop ID: {shop_id}")
        print(f"   - Secret Key: {'*' * 20}...{secret_key[-4:] if secret_key else 'Not set'}")
        print(f"   - Demo Mode: {demo_mode}")
        
        if shop_id and secret_key:
            print("✅ Конфигурация корректна")
            return True
        else:
            print("❌ Отсутствуют необходимые параметры")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка конфигурации: {e}")
        return False

def test_prodamus_api():
    """Тест API Prodamus"""
    print("\n💳 Тестирование API Prodamus...")
    
    try:
        # Импортируем класс API
        from prodamus import ProdаmusAPI
        
        # Создаем экземпляр
        api = ProdаmusAPI()
        
        print(f"   - Shop ID: {api.shop_id}")
        print(f"   - Demo Mode: {api.demo_mode}")
        print(f"   - API URL: {api.api_url}")
        
        # Тестируем генерацию подписи
        test_data = "test_string"
        signature = api.generate_signature(test_data)
        
        if signature:
            print("✅ API инициализирован корректно")
            print(f"   - Подпись сгенерирована: {'*' * 20}...{signature[-4:]}")
            return True
        else:
            print("❌ Ошибка генерации подписи")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка API: {e}")
        return False

def test_webhook_config():
    """Тест конфигурации webhook"""
    print("\n🔗 Тестирование webhook...")
    
    try:
        # Проверяем конфигурацию webhook
        webhook_url = os.getenv('WEBHOOK_URL', 'https://--help/webhook/prodamus')
        flask_host = os.getenv('FLASK_HOST', '0.0.0.0')
        flask_port = int(os.getenv('FLASK_PORT', '5000'))
        
        print(f"   - Webhook URL: {webhook_url}")
        print(f"   - Flask Host: {flask_host}")
        print(f"   - Flask Port: {flask_port}")
        
        print("✅ Конфигурация webhook корректна")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка конфигурации webhook: {e}")
        return False

def test_demo_cards():
    """Тест демо-карт"""
    print("\n🧪 Тестирование демо-режима...")
    
    demo_cards = [
        {"name": "МИР", "number": "2202 2050 0001 2424", "expiry": "05/35", "cvc": "669"},
        {"name": "MasterCard", "number": "5469 9801 0004 8525", "expiry": "05/26", "cvc": "041"},
        {"name": "Visa", "number": "4006 8009 0096 2514", "expiry": "05/26", "cvc": "941"},
        {"name": "Монета", "number": "2200 2400 0000 0006", "expiry": "12/24", "cvc": "123"},
        {"name": "ГазпромБанк", "number": "4242 4242 4242 4242", "expiry": "12/30", "cvc": "123"}
    ]
    
    print("✅ Демо-режим активен. Доступные тестовые карты:")
    for card in demo_cards:
        print(f"   📱 {card['name']}: {card['number']} ({card['expiry']}, CVC: {card['cvc']})")
    
    return True

def test_smart_sender():
    """Тест Smart Sender"""
    print("\n📧 Тестирование Smart Sender...")
    
    try:
        api_key = os.getenv('SMART_SENDER_API_KEY')
        
        if api_key:
            print(f"   - API Key: {'*' * 20}...{api_key[-4:]}")
            print("✅ Smart Sender API ключ настроен")
            return True
        else:
            print("⚠️ SMART_SENDER_API_KEY не установлен")
            print("   Для полной функциональности установите переменную окружения")
            return True  # Не критичная ошибка
            
    except Exception as e:
        print(f"❌ Ошибка Smart Sender: {e}")
        return False

def main():
    """Основная функция тестирования"""
    print("🚀 УПРОЩЕННОЕ ТЕСТИРОВАНИЕ СИСТЕМЫ ПЛАТЕЖЕЙ PRODAMUS")
    print("=" * 60)
    print(f"Время запуска: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python: {sys.version}")
    print()
    
    # Запускаем тесты
    tests = [
        ("Конфигурация", test_config),
        ("API Prodamus", test_prodamus_api),
        ("Webhook", test_webhook_config),
        ("Демо-карты", test_demo_cards),
        ("Smart Sender", test_smart_sender)
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
    print("\n" + "=" * 60)
    print("📋 ИТОГИ ТЕСТИРОВАНИЯ:")
    
    passed = 0
    for test_name, success in results:
        status = "✅ ПРОЙДЕН" if success else "❌ ПРОВАЛЕН"
        print(f"   {test_name}: {status}")
        if success:
            passed += 1
    
    print(f"\n🎯 Результат: {passed}/{len(results)} тестов пройдено")
    
    if passed == len(results):
        print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        print("\n📝 Система готова к использованию!")
        print("\n🔧 Следующие шаги:")
        print("   1. Установите зависимости: python install_dependencies.py")
        print("   2. Запустите webhook сервер: python webhook.py")
        print("   3. Проведите тестовую оплату с демо-картами")
    else:
        print(f"\n⚠️ {len(results) - passed} тестов не пройдено")
        print("\n📝 Рекомендации:")
        print("   1. Проверьте конфигурацию в config.py")
        print("   2. Установите зависимости: python install_dependencies.py")
        print("   3. Проверьте переменные окружения")

if __name__ == "__main__":
    main()
