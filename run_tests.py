#!/usr/bin/env python3
"""
Основной скрипт для запуска всех тестов системы платежей Prodamus
"""

import os
import sys
import subprocess
import time
from datetime import datetime

def print_header(title):
    """Печать заголовка"""
    print("\n" + "=" * 60)
    print(f"🚀 {title}")
    print("=" * 60)

def print_section(title):
    """Печать заголовка секции"""
    print(f"\n📋 {title}")
    print("-" * 40)

def run_test_script(script_name, description):
    """Запуск тестового скрипта"""
    print_section(description)
    
    try:
        # Проверяем существование файла
        if not os.path.exists(script_name):
            print(f"❌ Файл {script_name} не найден")
            return False
        
        # Запускаем скрипт
        result = subprocess.run([sys.executable, script_name], 
                               capture_output=True, text=True, timeout=60)
        
        # Выводим результат
        if result.stdout:
            print(result.stdout)
        
        if result.stderr:
            print("STDERR:", result.stderr)
        
        if result.returncode == 0:
            print(f"✅ {description} - ПРОЙДЕН")
            return True
        else:
            print(f"❌ {description} - ПРОВАЛЕН (код: {result.returncode})")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {description} - ТАЙМАУТ")
        return False
    except Exception as e:
        print(f"❌ Ошибка запуска {description}: {e}")
        return False

def check_environment():
    """Проверка окружения"""
    print_section("Проверка окружения")
    
    # Проверяем Python
    python_version = sys.version_info
    print(f"Python: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Проверяем необходимые файлы
    required_files = [
        'config.py',
        'prodamus.py',
        'webhook.py',
        'database.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Отсутствуют файлы: {', '.join(missing_files)}")
        return False
    else:
        print("✅ Все необходимые файлы найдены")
    
    # Проверяем переменные окружения
    env_vars = [
        'PRODAMUS_SECRET_KEY',
        'SMART_SENDER_API_KEY'
    ]
    
    missing_vars = []
    for var in env_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️ Отсутствуют переменные окружения: {', '.join(missing_vars)}")
        print("   Используются значения по умолчанию из config.py")
    else:
        print("✅ Все переменные окружения установлены")
    
    return True

def main():
    """Основная функция"""
    print_header("ТЕСТИРОВАНИЕ СИСТЕМЫ ПЛАТЕЖЕЙ PRODAMUS")
    print(f"Время запуска: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Проверяем окружение
    if not check_environment():
        print("\n❌ Проблемы с окружением. Исправьте ошибки и запустите снова.")
        return
    
    # Список тестов
    tests = [
        ('test_prodamus_integration.py', 'Интеграция с Prodamus API'),
        ('test_webhook.py', 'Webhook обработка'),
        ('smart_sender_integration.py', 'Интеграция с Smart Sender')
    ]
    
    # Запускаем тесты
    results = []
    
    for script, description in tests:
        success = run_test_script(script, description)
        results.append((description, success))
    
    # Выводим итоги
    print_header("ИТОГИ ТЕСТИРОВАНИЯ")
    
    passed = 0
    total = len(results)
    
    for description, success in results:
        status = "✅ ПРОЙДЕН" if success else "❌ ПРОВАЛЕН"
        print(f"   {description}: {status}")
        if success:
            passed += 1
    
    print(f"\n🎯 Общий результат: {passed}/{total} тестов пройдено")
    
    if passed == total:
        print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        print("\n📝 Следующие шаги:")
        print("   1. Настройте webhook URL в панели Prodamus")
        print("   2. Проведите тестовую оплату с тестовыми картами:")
        print("      • МИР: 2202 2050 0001 2424 (05/35, CVC: 669)")
        print("      • MasterCard: 5469 9801 0004 8525 (05/26, CVC: 041)")
        print("      • Visa: 4006 8009 0096 2514 (05/26, CVC: 941)")
        print("   3. Проверьте получение уведомлений в webhook")
        print("   4. Протестируйте интеграцию с Smart Sender")
    else:
        print(f"\n⚠️ {total - passed} тестов не пройдено")
        print("\n📝 Рекомендации:")
        print("   1. Проверьте конфигурацию в config.py")
        print("   2. Убедитесь, что все зависимости установлены")
        print("   3. Проверьте переменные окружения")
        print("   4. Убедитесь, что webhook сервер запущен")

if __name__ == "__main__":
    main()
