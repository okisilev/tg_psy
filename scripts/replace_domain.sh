#!/bin/bash

# 🌐 СКРИПТ ЗАМЕНЫ ДОМЕНА
# Использование: ./replace_domain.sh yourdomain.com

if [ $# -eq 0 ]; then
    echo "❌ Ошибка: Укажите домен"
    echo "Использование: ./replace_domain.sh yourdomain.com"
    echo "Пример: ./replace_domain.sh mydomain.com"
    exit 1
fi

DOMAIN=$1

echo "🌐 Замена домена на: $DOMAIN"
echo "=" * 60

# Обновляем переменные окружения
export WEBHOOK_URL="https://$DOMAIN/webhook/telegram"
export PRODAMUS_WEBHOOK_URL="https://$DOMAIN/webhook/prodamus"

echo "✅ Переменные окружения обновлены:"
echo "   - WEBHOOK_URL: $WEBHOOK_URL"
echo "   - PRODAMUS_WEBHOOK_URL: $PRODAMUS_WEBHOOK_URL"

# Обновляем .env файл
if [ -f .env ]; then
    sed -i.bak "s/yourdomain.com/$DOMAIN/g" .env
    echo "✅ .env файл обновлен"
fi

# Обновляем config.py
if [ -f config.py ]; then
    sed -i.bak "s/yourdomain.com/$DOMAIN/g" config.py
    echo "✅ config.py обновлен"
fi

# Обновляем QUICK_ENV_SETUP.sh
if [ -f QUICK_ENV_SETUP.sh ]; then
    sed -i.bak "s/yourdomain.com/$DOMAIN/g" QUICK_ENV_SETUP.sh
    echo "✅ QUICK_ENV_SETUP.sh обновлен"
fi

echo ""
echo "🔍 Проверка конфигурации:"
python3 check_config.py

echo ""
echo "🎉 Домен $DOMAIN настроен!"
echo ""
echo "📝 Следующие шаги:"
echo "   1. Настройте SSL сертификат для домена"
echo "   2. Настройте Nginx/Apache для проксирования"
echo "   3. Запустите webhook сервер: python3 start_webhook.py"
echo "   4. Настройте webhook URL в панели Prodamus"
