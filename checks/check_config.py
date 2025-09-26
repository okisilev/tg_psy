#!/usr/bin/env python3
"""
Скрипт для проверки конфигурации системы
"""

import os
import sys
from datetime import datetime

def check_telegram_config():
    """Проверка конфигурации Telegram бота"""
    print("🤖 Проверка конфигурации Telegram бота...")
    print("-" * 50)
    
    bot_token = os.getenv('BOT_TOKEN')
    admin_chat_id = os.getenv('ADMIN_CHAT_ID')
    admin_ids = os.getenv('ADMIN_IDS', '').split(',') if os.getenv('ADMIN_IDS') else []
    channel_id = os.getenv('CHANNEL_ID')
    channel_username = os.getenv('CHANNEL_USERNAME')
    channel_invite_link = os.getenv('CHANNEL_INVITE_LINK')
    
    print(f"   - BOT_TOKEN: {'✅ Установлен' if bot_token else '❌ Не установлен'}")
    print(f"   - ADMIN_CHAT_ID: {'✅ Установлен' if admin_chat_id else '❌ Не установлен'}")
    print(f"   - ADMIN_IDS: {'✅ Установлен' if admin_ids else '❌ Не установлен'}")
    print(f"   - CHANNEL_ID: {'✅ Установлен' if channel_id else '❌ Не установлен'}")
    print(f"   - CHANNEL_USERNAME: {'✅ Установлен' if channel_username else '❌ Не установлен'}")
    print(f"   - CHANNEL_INVITE_LINK: {'✅ Установлен' if channel_invite_link else '❌ Не установлен'}")
    
    # Проверяем, что ID канала не тестовый
    if channel_id == '-1001234567890' or channel_id == 'your_channel_id_here':
        print("   ⚠️ CHANNEL_ID использует тестовое значение - замените на реальный ID канала")
    
    return all([bot_token, admin_chat_id, admin_ids, channel_id])

def check_prodamus_config():
    """Проверка конфигурации Prodamus"""
    print("\n💳 Проверка конфигурации Prodamus...")
    print("-" * 50)
    
    shop_id = os.getenv('PRODAMUS_SHOP_ID')
    secret_key = os.getenv('PRODAMUS_SECRET_KEY')
    demo_mode = os.getenv('PRODAMUS_DEMO_MODE', 'true').lower() == 'true'
    webhook_url = os.getenv('PRODAMUS_WEBHOOK_URL')
    
    print(f"   - PRODAMUS_SHOP_ID: {'✅ Установлен' if shop_id else '❌ Не установлен'}")
    print(f"   - PRODAMUS_SECRET_KEY: {'✅ Установлен' if secret_key else '❌ Не установлен'}")
    print(f"   - PRODAMUS_DEMO_MODE: {'✅ Включен' if demo_mode else '❌ Отключен'}")
    print(f"   - PRODAMUS_WEBHOOK_URL: {'✅ Установлен' if webhook_url else '❌ Не установлен'}")
    
    # Проверяем webhook URL
    if webhook_url and 'yourdomain.com' in webhook_url:
        print("   ⚠️ PRODAMUS_WEBHOOK_URL использует тестовое значение - замените на реальный домен")
    
    return all([shop_id, secret_key, webhook_url])

def check_webhook_config():
    """Проверка конфигурации webhook"""
    print("\n🔗 Проверка конфигурации webhook...")
    print("-" * 50)
    
    webhook_url = os.getenv('WEBHOOK_URL')
    prodamus_webhook_url = os.getenv('PRODAMUS_WEBHOOK_URL')
    flask_host = os.getenv('FLASK_HOST', '0.0.0.0')
    flask_port = int(os.getenv('FLASK_PORT', '5000'))
    
    print(f"   - WEBHOOK_URL: {'✅ Установлен' if webhook_url else '❌ Не установлен'}")
    print(f"   - PRODAMUS_WEBHOOK_URL: {'✅ Установлен' if prodamus_webhook_url else '❌ Не установлен'}")
    print(f"   - FLASK_HOST: {flask_host}")
    print(f"   - FLASK_PORT: {flask_port}")
    
    # Проверяем URL
    if webhook_url and 'yourdomain.com' in webhook_url:
        print("   ⚠️ WEBHOOK_URL использует тестовое значение - замените на реальный домен")
    
    if prodamus_webhook_url and 'yourdomain.com' in prodamus_webhook_url:
        print("   ⚠️ PRODAMUS_WEBHOOK_URL использует тестовое значение - замените на реальный домен")
    
    return all([webhook_url, prodamus_webhook_url])

def check_domain_setup():
    """Проверка настройки домена"""
    print("\n🌐 Проверка настройки домена...")
    print("-" * 50)
    
    webhook_url = os.getenv('WEBHOOK_URL')
    prodamus_webhook_url = os.getenv('PRODAMUS_WEBHOOK_URL')
    
    if webhook_url and 'yourdomain.com' in webhook_url:
        print("   ❌ Домен не настроен - замените 'yourdomain.com' на реальный домен")
        print("   📝 Примеры доменов:")
        print("      - https://yourdomain.com/webhook/telegram")
        print("      - https://yourdomain.com/webhook/prodamus")
        return False
    else:
        print("   ✅ Домен настроен")
        return True

def check_ssl_setup():
    """Проверка настройки SSL"""
    print("\n🔒 Проверка настройки SSL...")
    print("-" * 50)
    
    webhook_url = os.getenv('WEBHOOK_URL')
    
    if webhook_url and webhook_url.startswith('https://'):
        print("   ✅ HTTPS настроен")
        return True
    else:
        print("   ⚠️ HTTPS не настроен - рекомендуется использовать HTTPS для webhook")
        return False

def main():
    """Основная функция проверки"""
    print("🔍 ПРОВЕРКА КОНФИГУРАЦИИ СИСТЕМЫ")
    print("=" * 60)
    print(f"Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Запускаем проверки
    checks = [
        ("Telegram Bot", check_telegram_config),
        ("Prodamus", check_prodamus_config),
        ("Webhook", check_webhook_config),
        ("Домен", check_domain_setup),
        ("SSL", check_ssl_setup)
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
        print("📝 Система готова к запуску:")
        print("   1. Запустите webhook сервер: python3 start_webhook.py")
        print("   2. Настройте webhook URL в панели Prodamus")
        print("   3. Протестируйте создание платежа")
    else:
        print(f"\n⚠️ {len(results) - passed} проверок не пройдено")
        print("\n📝 Рекомендации:")
        print("   1. Настройте реальный домен в переменных окружения")
        print("   2. Установите реальный CHANNEL_ID")
        print("   3. Настройте SSL сертификат")
        print("   4. Проверьте права бота в канале")

if __name__ == "__main__":
    main()
