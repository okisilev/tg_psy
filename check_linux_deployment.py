#!/usr/bin/env python3
"""
Скрипт проверки готовности к развертыванию на Linux сервере
"""

import os
import sys
import subprocess
import platform
from datetime import datetime

def check_system_requirements():
    """Проверка системных требований"""
    print("🖥️ ПРОВЕРКА СИСТЕМНЫХ ТРЕБОВАНИЙ")
    print("-" * 50)
    
    # Проверка ОС
    system = platform.system()
    print(f"   - Операционная система: {system}")
    
    if system != "Linux":
        print("   ⚠️ Внимание: Скрипт предназначен для Linux")
    
    # Проверка Python версии
    python_version = sys.version_info
    print(f"   - Python версия: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 8):
        print("   ❌ Требуется Python 3.8+")
        return False
    else:
        print("   ✅ Python версия подходит")
    
    # Проверка доступных портов
    print("\n🔌 ПРОВЕРКА ПОРТОВ")
    print("-" * 50)
    
    ports_to_check = [80, 443, 5000]
    for port in ports_to_check:
        try:
            result = subprocess.run(['netstat', '-tlnp'], capture_output=True, text=True)
            if f":{port}" in result.stdout:
                print(f"   ⚠️ Порт {port} уже занят")
            else:
                print(f"   ✅ Порт {port} свободен")
        except:
            print(f"   ❓ Не удалось проверить порт {port}")
    
    return True

def check_python_packages():
    """Проверка Python пакетов"""
    print("\n📦 ПРОВЕРКА PYTHON ПАКЕТОВ")
    print("-" * 50)
    
    required_packages = [
        'flask',
        'requests',
        'python-telegram-bot',
        'sqlite3',
        'hmac',
        'hashlib'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - не установлен")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n   📝 Установите недостающие пакеты:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False
    
    return True

def check_configuration():
    """Проверка конфигурации"""
    print("\n⚙️ ПРОВЕРКА КОНФИГУРАЦИИ")
    print("-" * 50)
    
    # Проверка переменных окружения
    required_env_vars = [
        'BOT_TOKEN',
        'ADMIN_CHAT_ID',
        'CHANNEL_ID',
        'PRODAMUS_SHOP_ID',
        'PRODAMUS_SECRET_KEY',
        'PRODAMUS_WEBHOOK_URL'
    ]
    
    missing_vars = []
    
    for var in required_env_vars:
        if os.getenv(var):
            print(f"   ✅ {var}")
        else:
            print(f"   ❌ {var} - не установлена")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n   📝 Установите недостающие переменные окружения:")
        for var in missing_vars:
            print(f"   export {var}=\"your_value_here\"")
        return False
    
    return True

def check_files():
    """Проверка файлов проекта"""
    print("\n📁 ПРОВЕРКА ФАЙЛОВ ПРОЕКТА")
    print("-" * 50)
    
    required_files = [
        'config.py',
        'bot.py',
        'webhook_http.py',
        'prodamus.py',
        'database.py',
        'channel_manager.py',
        'main.py'
    ]
    
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} - не найден")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n   📝 Отсутствуют файлы: {', '.join(missing_files)}")
        return False
    
    return True

def check_database():
    """Проверка базы данных"""
    print("\n🗄️ ПРОВЕРКА БАЗЫ ДАННЫХ")
    print("-" * 50)
    
    try:
        from database import Database
        db = Database()
        print("   ✅ База данных инициализирована")
        
        # Проверка таблиц
        import sqlite3
        conn = sqlite3.connect('women_club.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        expected_tables = ['users', 'subscriptions', 'payments']
        existing_tables = [table[0] for table in tables]
        
        for table in expected_tables:
            if table in existing_tables:
                print(f"   ✅ Таблица {table}")
            else:
                print(f"   ❌ Таблица {table} - не найдена")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"   ❌ Ошибка базы данных: {e}")
        return False

def check_webhook_config():
    """Проверка конфигурации webhook"""
    print("\n🔗 ПРОВЕРКА КОНФИГУРАЦИИ WEBHOOK")
    print("-" * 50)
    
    try:
        from config import PRODAMUS_WEBHOOK_URL, FLASK_HOST, FLASK_PORT
        
        print(f"   - Webhook URL: {PRODAMUS_WEBHOOK_URL}")
        print(f"   - Flask Host: {FLASK_HOST}")
        print(f"   - Flask Port: {FLASK_PORT}")
        
        # Проверка URL
        if 'yourdomain.com' in PRODAMUS_WEBHOOK_URL:
            print("   ⚠️ Замените yourdomain.com на реальный домен")
            return False
        
        if not PRODAMUS_WEBHOOK_URL.startswith('http'):
            print("   ❌ Webhook URL должен начинаться с http:// или https://")
            return False
        
        print("   ✅ Конфигурация webhook корректна")
        return True
        
    except Exception as e:
        print(f"   ❌ Ошибка конфигурации webhook: {e}")
        return False

def check_linux_specific():
    """Проверка Linux-специфичных настроек"""
    print("\n🐧 ПРОВЕРКА LINUX НАСТРОЕК")
    print("-" * 50)
    
    # Проверка прав доступа
    try:
        if os.access('.', os.W_OK):
            print("   ✅ Права на запись в директорию")
        else:
            print("   ❌ Нет прав на запись в директорию")
            return False
    except:
        print("   ❓ Не удалось проверить права доступа")
    
    # Проверка systemd (если доступен)
    try:
        result = subprocess.run(['systemctl', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("   ✅ Systemd доступен")
        else:
            print("   ⚠️ Systemd недоступен")
    except:
        print("   ❓ Systemd не найден")
    
    # Проверка Nginx (если установлен)
    try:
        result = subprocess.run(['nginx', '-v'], capture_output=True, text=True)
        if result.returncode == 0:
            print("   ✅ Nginx установлен")
        else:
            print("   ⚠️ Nginx не установлен")
    except:
        print("   ❓ Nginx не найден")
    
    return True

def main():
    """Основная функция проверки"""
    print("🔍 ПРОВЕРКА ГОТОВНОСТИ К РАЗВЕРТЫВАНИЮ НА LINUX")
    print("=" * 60)
    print(f"Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    checks = [
        ("Системные требования", check_system_requirements),
        ("Python пакеты", check_python_packages),
        ("Конфигурация", check_configuration),
        ("Файлы проекта", check_files),
        ("База данных", check_database),
        ("Webhook конфигурация", check_webhook_config),
        ("Linux настройки", check_linux_specific)
    ]
    
    results = []
    
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"❌ Ошибка в проверке '{check_name}': {e}")
            results.append((check_name, False))
    
    # Выводим итоги
    print("\n" + "=" * 60)
    print("📋 ИТОГИ ПРОВЕРКИ:")
    
    passed = 0
    for check_name, success in results:
        status = "✅ ПРОЙДЕН" if success else "❌ ПРОВАЛЕН"
        print(f"   {check_name}: {status}")
        if success:
            passed += 1
    
    print(f"\n🎯 Результат: {passed}/{len(results)} проверок пройдено")
    
    if passed == len(results):
        print("\n🎉 ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ!")
        print("📝 Система готова к развертыванию на Linux сервере:")
        print("   1. Загрузите файлы на сервер")
        print("   2. Установите зависимости")
        print("   3. Настройте переменные окружения")
        print("   4. Настройте Nginx и SSL")
        print("   5. Запустите сервисы")
    else:
        print(f"\n⚠️ {len(results) - passed} проверок не пройдено")
        print("\n📝 Рекомендации:")
        print("   1. Установите недостающие пакеты")
        print("   2. Настройте переменные окружения")
        print("   3. Проверьте конфигурацию")
        print("   4. Убедитесь, что все файлы на месте")

if __name__ == "__main__":
    main()
