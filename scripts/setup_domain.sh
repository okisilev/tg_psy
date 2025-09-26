#!/bin/bash

# 🚀 СКРИПТ НАСТРОЙКИ ДОМЕНА: --help
# Автоматически создан: 2025-09-19 13:07:10

echo "🌐 Настройка домена: --help"
echo "=" * 60

# 1. Обновление переменных окружения
export WEBHOOK_URL="https://--help/webhook/telegram"
export PRODAMUS_WEBHOOK_URL="https://--help/webhook/prodamus"

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
echo "🎉 Домен --help настроен!"
echo ""
echo "📝 Следующие шаги:"
echo "   1. Настройте SSL сертификат для домена"
echo "   2. Настройте Nginx/Apache для проксирования"
echo "   3. Запустите webhook сервер: python3 start_webhook.py"
echo "   4. Настройте webhook URL в панели Prodamus"
