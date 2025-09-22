#!/usr/bin/env python3
"""
Скрипт для замены yourdomain.com на реальный домен
"""

import os
import sys
import re
from datetime import datetime

def update_domain_files(domain):
    """Обновление домена во всех файлах"""
    print(f"🌐 Обновление домена на: {domain}")
    print("=" * 60)
    
    # Файлы для обновления
    files_to_update = [
        'config.py',
        '.env',
        'QUICK_ENV_SETUP.sh',
        'ENV_SETUP.md',
        'WEBHOOK_SETUP.md',
        'FINAL_SETUP_REPORT.md',
        'PAYMENT_GUIDE.md',
        'FINAL_SUMMARY.md',
        'simple_test.py',
        'QUICK_START.md',
        'PRODAMUS_SETUP_REPORT.md',
        'PRODAMUS_SETUP_GUIDE.md',
        'setup_production.md',
        'env_production_example',
        'deploy.sh',
        'README.md',
        'PRODUCTION_DEPLOYMENT.md',
        'SETUP_GUIDE.md',
        'nginx_config.conf'
    ]
    
    updated_files = []
    
    for filename in files_to_update:
        if os.path.exists(filename):
            try:
                # Читаем файл
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Заменяем домен
                old_content = content
                content = content.replace('yourdomain.com', domain)
                
                # Если содержимое изменилось, записываем обратно
                if content != old_content:
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(content)
                    updated_files.append(filename)
                    print(f"   ✅ {filename}")
                else:
                    print(f"   ⏭️ {filename} (не требует изменений)")
                    
            except Exception as e:
                print(f"   ❌ {filename}: {e}")
        else:
            print(f"   ⚠️ {filename} (файл не найден)")
    
    return updated_files

def update_environment_variables(domain):
    """Обновление переменных окружения"""
    print(f"\n🔧 Обновление переменных окружения...")
    
    # Обновляем переменные окружения
    os.environ['WEBHOOK_URL'] = f'https://{domain}/webhook/telegram'
    os.environ['PRODAMUS_WEBHOOK_URL'] = f'https://{domain}/webhook/prodamus'
    
    print(f"   ✅ WEBHOOK_URL: {os.environ['WEBHOOK_URL']}")
    print(f"   ✅ PRODAMUS_WEBHOOK_URL: {os.environ['PRODAMUS_WEBHOOK_URL']}")

def create_domain_setup_script(domain):
    """Создание скрипта для настройки домена"""
    script_content = f'''#!/bin/bash

# 🚀 СКРИПТ НАСТРОЙКИ ДОМЕНА: {domain}
# Автоматически создан: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

echo "🌐 Настройка домена: {domain}"
echo "=" * 60

# 1. Обновление переменных окружения
export WEBHOOK_URL="https://{domain}/webhook/telegram"
export PRODAMUS_WEBHOOK_URL="https://{domain}/webhook/prodamus"

echo "✅ Переменные окружения обновлены:"
echo "   - WEBHOOK_URL: $WEBHOOK_URL"
echo "   - PRODAMUS_WEBHOOK_URL: $PRODAMUS_WEBHOOK_URL"

# 2. Проверка конфигурации
echo ""
echo "🔍 Проверка конфигурации:"
python3 check_config.py

# 3. Тест создания платежа
echo ""
echo "🧪 Тест создания платежа:"
python3 test_payment_creation.py

echo ""
echo "🎉 Домен {domain} настроен!"
echo ""
echo "📝 Следующие шаги:"
echo "   1. Настройте SSL сертификат для домена"
echo "   2. Настройте Nginx/Apache для проксирования"
echo "   3. Запустите webhook сервер: python3 start_webhook.py"
echo "   4. Настройте webhook URL в панели Prodamus"
'''
    
    with open('setup_domain.sh', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    # Делаем скрипт исполняемым
    os.chmod('setup_domain.sh', 0o755)
    
    print(f"   ✅ Создан скрипт setup_domain.sh")

def main():
    """Основная функция"""
    print("🌐 НАСТРОЙКА ДОМЕНА")
    print("=" * 60)
    print(f"Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Получаем домен от пользователя
    if len(sys.argv) > 1:
        domain = sys.argv[1]
    else:
        domain = input("Введите ваш домен (без https://): ").strip()
    
    if not domain:
        print("❌ Домен не указан!")
        return
    
    # Убираем https:// если есть
    domain = domain.replace('https://', '').replace('http://', '')
    
    print(f"🎯 Настраиваем домен: {domain}")
    print()
    
    # Обновляем файлы
    updated_files = update_domain_files(domain)
    
    # Обновляем переменные окружения
    update_environment_variables(domain)
    
    # Создаем скрипт настройки
    create_domain_setup_script(domain)
    
    print(f"\n✅ ОБНОВЛЕНИЕ ЗАВЕРШЕНО!")
    print(f"📁 Обновлено файлов: {len(updated_files)}")
    print()
    print("📝 Следующие шаги:")
    print("   1. Запустите: ./setup_domain.sh")
    print("   2. Настройте SSL сертификат")
    print("   3. Настройте Nginx/Apache")
    print("   4. Запустите webhook сервер")
    print("   5. Настройте webhook URL в панели Prodamus")

if __name__ == "__main__":
    main()
