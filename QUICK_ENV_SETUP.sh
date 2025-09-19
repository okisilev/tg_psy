#!/bin/bash

# 🚀 БЫСТРАЯ НАСТРОЙКА ПЕРЕМЕННЫХ ОКРУЖЕНИЯ
# Скрипт для быстрой настройки всех необходимых переменных

echo "🔧 Настройка переменных окружения для системы платежей..."

# Telegram Bot Configuration
export BOT_TOKEN="8455794146:AAFf9DEcTxLnJfG-HWWmzwpSjTRDzNE3px8"
export ADMIN_CHAT_ID="431292182,190545165"
export ADMIN_IDS="431292182,190545165"
export CHANNEL_ID="-1001234567890"  # ⚠️ ЗАМЕНИТЕ НА РЕАЛЬНЫЙ ID КАНАЛА
export CHANNEL_USERNAME="@your_channel_username"  # ⚠️ ЗАМЕНИТЕ НА РЕАЛЬНЫЙ USERNAME
export CHANNEL_INVITE_LINK="https://t.me/+gstVWYW2Kgo2OGYy"  # ⚠️ ЗАМЕНИТЕ НА РЕАЛЬНУЮ ССЫЛКУ

# Prodamus Configuration
export PRODAMUS_SHOP_ID="dashastar"
export PRODAMUS_SECRET_KEY="b2f9e8a399225271521dfe88a277a7371cb8c2cebfeaa6f0276ba81fcc303c93"
export PRODAMUS_DEMO_MODE="true"
export PRODAMUS_WEBHOOK_URL="https://yourdomain.com/webhook/prodamus"  # ⚠️ ЗАМЕНИТЕ НА РЕАЛЬНЫЙ ДОМЕН

# Webhook Configuration
export WEBHOOK_URL="https://yourdomain.com/webhook/telegram"  # ⚠️ ЗАМЕНИТЕ НА РЕАЛЬНЫЙ ДОМЕН
export FLASK_HOST="0.0.0.0"
export FLASK_PORT="5000"
export DEBUG="false"

echo "✅ Переменные окружения установлены!"
echo ""
echo "⚠️ ВАЖНО: Замените следующие значения на реальные:"
echo "   - CHANNEL_ID: -1001234567890 → Реальный ID канала"
echo "   - CHANNEL_USERNAME: @your_channel_username → Реальный username"
echo "   - CHANNEL_INVITE_LINK: https://t.me/+gstVWYW2Kgo2OGYy → Реальная ссылка"
echo "   - yourdomain.com → Ваш реальный домен"
echo ""
echo "🔍 Проверка конфигурации:"
python3 check_config.py
echo ""
echo "🧪 Тест создания платежа:"
python3 test_payment_creation.py
echo ""
echo "🚀 Запуск webhook сервера:"
echo "python3 start_webhook.py"
echo ""
echo "📝 Документация:"
echo "   - ENV_SETUP.md - Подробная настройка"
echo "   - WEBHOOK_SETUP.md - Настройка webhook"
echo "   - FINAL_SETUP_REPORT.md - Итоговый отчет"
