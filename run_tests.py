#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Запуск всех тестов проекта
"""

import os
import sys
import subprocess
import time

def run_test(test_file):
    """Запуск одного теста"""
    print(f"\n🧪 Запуск теста: {test_file}")
    print("=" * 60)
    
    try:
        result = subprocess.run([sys.executable, test_file], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print(f"✅ {test_file} - ПРОЙДЕН")
            return True
        else:
            print(f"❌ {test_file} - ОШИБКА")
            print(f"   Ошибка: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {test_file} - ТАЙМАУТ")
        return False
    except Exception as e:
        print(f"💥 {test_file} - ИСКЛЮЧЕНИЕ: {e}")
        return False

def main():
    """Запуск всех тестов"""
    print("🧪 ЗАПУСК ВСЕХ ТЕСТОВ ПРОЕКТА")
    print("=" * 60)
    
    # Список тестов для запуска
    tests = [
        "tests/test_contact_verification.py",
        "tests/test_webhook.py", 
        "tests/test_payment_check.py",
        "tests/test_prodamus_webhook.py"
    ]
    
    # Проверяем существование тестов
    existing_tests = []
    for test in tests:
        if os.path.exists(test):
            existing_tests.append(test)
        else:
            print(f"⚠️ Тест не найден: {test}")
    
    if not existing_tests:
        print("❌ Тесты не найдены!")
        return
    
    print(f"📋 Найдено тестов: {len(existing_tests)}")
    
    # Запускаем тесты
    passed = 0
    failed = 0
    
    for test in existing_tests:
        if run_test(test):
            passed += 1
        else:
            failed += 1
        
        time.sleep(1)  # Пауза между тестами
    
    # Результаты
    print("\n" + "=" * 60)
    print("📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
    print("=" * 60)
    print(f"✅ Пройдено: {passed}")
    print(f"❌ Провалено: {failed}")
    print(f"📋 Всего: {passed + failed}")
    
    if failed == 0:
        print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
    else:
        print(f"\n⚠️ {failed} ТЕСТОВ ПРОВАЛЕНО")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)