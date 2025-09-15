#!/usr/bin/env python3
"""
Простой скрипт для запуска бота
"""

import os
import sys

def check_requirements():
    """Проверка наличия необходимых файлов"""
    required_files = [
        '.env',
        'config.py',
        'database.py',
        'bot.py',
        'prodamus.py',
        'scheduler.py',
        'admin_panel.py',
        'channel_manager.py',
        'webhook.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Отсутствуют необходимые файлы:")
        for file in missing_files:
            print(f"   - {file}")
        print("\nУбедитесь, что вы находитесь в правильной директории проекта.")
        return False
    
    return True

def check_env_file():
    """Проверка файла .env"""
    if not os.path.exists('.env'):
        print("❌ Файл .env не найден!")
        print("Скопируйте env_example.txt в .env и заполните необходимые параметры:")
        print("   cp env_example.txt .env")
        return False
    
    return True

def main():
    """Главная функция"""
    print("🤖 Запуск Telegram бота для Женского клуба")
    print("=" * 50)
    
    # Проверяем файлы
    if not check_requirements():
        sys.exit(1)
    
    if not check_env_file():
        sys.exit(1)
    
    # Инициализируем базу данных
    print("📊 Инициализация базы данных...")
    try:
        from init_db import init_database
        init_database()
    except Exception as e:
        print(f"❌ Ошибка инициализации базы данных: {e}")
        sys.exit(1)
    
    # Тестируем конфигурацию
    print("🧪 Тестирование конфигурации...")
    try:
        from test_bot import test_config
        test_config()
        print("✅ Конфигурация в порядке")
    except Exception as e:
        print(f"⚠️ Проблемы с конфигурацией: {e}")
        print("Проверьте файл .env")
    
    # Запускаем бота
    print("\n🚀 Запуск бота...")
    try:
        from main import ApplicationManager
        app_manager = ApplicationManager()
        app_manager.start()
    except KeyboardInterrupt:
        print("\n👋 Бот остановлен пользователем")
    except Exception as e:
        print(f"\n❌ Ошибка запуска бота: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
