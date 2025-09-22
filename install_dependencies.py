#!/usr/bin/env python3
"""
Скрипт для установки зависимостей системы платежей Prodamus
"""

import subprocess
import sys
import os

def install_package(package):
    """Установка пакета через pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} установлен успешно")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка установки {package}: {e}")
        return False

def main():
    """Основная функция установки зависимостей"""
    print("🚀 Установка зависимостей для системы платежей Prodamus")
    print("=" * 60)
    
    # Список необходимых пакетов
    packages = [
        "python-dotenv",
        "requests",
        "flask",
        "hmac",
        "hashlib"
    ]
    
    print("📦 Устанавливаем необходимые пакеты...")
    
    success_count = 0
    for package in packages:
        if package in ["hmac", "hashlib"]:
            # Эти модули встроены в Python
            print(f"✅ {package} - встроенный модуль Python")
            success_count += 1
        else:
            if install_package(package):
                success_count += 1
    
    print(f"\n🎯 Результат: {success_count}/{len(packages)} пакетов установлено")
    
    if success_count == len(packages):
        print("🎉 Все зависимости установлены успешно!")
        print("\n📝 Теперь можно запустить тесты:")
        print("   python run_tests.py")
    else:
        print("⚠️ Некоторые пакеты не удалось установить.")
        print("   Попробуйте установить их вручную:")
        for package in packages:
            if package not in ["hmac", "hashlib"]:
                print(f"   pip install {package}")

if __name__ == "__main__":
    main()
