#!/usr/bin/env python3
"""
Скрипт для запуска webhook сервера Prodamus
"""

import os
import sys
import signal
import time
from datetime import datetime

def signal_handler(sig, frame):
    """Обработчик сигнала для корректного завершения"""
    print('\n🛑 Получен сигнал завершения. Останавливаем сервер...')
    sys.exit(0)

def check_dependencies():
    """Проверка зависимостей"""
    print("🔍 Проверка зависимостей...")
    
    missing_deps = []
    
    try:
        import flask
        print("✅ Flask установлен")
    except ImportError:
        missing_deps.append("flask")
    
    try:
        import requests
        print("✅ Requests установлен")
    except ImportError:
        missing_deps.append("requests")
    
    if missing_deps:
        print(f"❌ Отсутствуют зависимости: {', '.join(missing_deps)}")
        print("📦 Установите их командой:")
        print(f"   pip install {' '.join(missing_deps)}")
        return False
    
    print("✅ Все зависимости установлены")
    return True

def start_webhook_server():
    """Запуск webhook сервера"""
    print("🚀 Запуск webhook сервера Prodamus...")
    print("=" * 50)
    
    # Проверяем зависимости
    if not check_dependencies():
        return False
    
    # Настраиваем обработчик сигналов
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Импортируем и запускаем webhook
        from webhook import app, FLASK_HOST, FLASK_PORT
        
        print(f"🌐 Сервер запущен на {FLASK_HOST}:{FLASK_PORT}")
        print(f"📡 Webhook URL: http://{FLASK_HOST}:{FLASK_PORT}/webhook/prodamus")
        print(f"🏥 Health Check: http://{FLASK_HOST}:{FLASK_PORT}/health")
        print("\n📝 Для остановки нажмите Ctrl+C")
        print("=" * 50)
        
        # Запускаем сервер
        app.run(
            host=FLASK_HOST,
            port=FLASK_PORT,
            debug=False,
            threaded=True
        )
        
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        print("📝 Убедитесь, что файл webhook.py существует")
        return False
    except Exception as e:
        print(f"❌ Ошибка запуска сервера: {e}")
        return False

def main():
    """Основная функция"""
    print("🚀 WEBHOOK СЕРВЕР PRODAMUS")
    print("=" * 50)
    print(f"Время запуска: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python: {sys.version}")
    print()
    
    # Проверяем конфигурацию
    shop_id = os.getenv('PRODAMUS_SHOP_ID', 'dashastar')
    secret_key = os.getenv('PRODAMUS_SECRET_KEY', 'b2f9e8a399225271521dfe88a277a7371cb8c2cebfeaa6f0276ba81fcc303c93')
    
    print(f"🔧 Конфигурация:")
    print(f"   - Shop ID: {shop_id}")
    print(f"   - Secret Key: {'*' * 20}...{secret_key[-4:] if secret_key else 'Not set'}")
    print()
    
    # Запускаем сервер
    if start_webhook_server():
        print("✅ Сервер запущен успешно")
    else:
        print("❌ Ошибка запуска сервера")
        sys.exit(1)

if __name__ == "__main__":
    main()
