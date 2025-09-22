#!/bin/bash

# 🔧 ВРЕМЕННОЕ ИСПОЛЬЗОВАНИЕ IP WEBHOOK
# Временное использование IP адреса вместо PageKite

echo "🔧 ВРЕМЕННОЕ ИСПОЛЬЗОВАНИЕ IP WEBHOOK"
echo "=" * 50

# 1. Остановка webhook сервера
echo "⏹️ Остановка webhook сервера..."
pkill -f webhook.py
sleep 3

# 2. Обновление .env файла для использования IP
echo "📝 Обновление .env файла для использования IP..."
cat > .env << 'EOF'
# Telegram Bot Configuration
BOT_TOKEN=8455794146:AAFf9DEcTxLnJfG-HWWmzwpSjTRDzNE3px8
ADMIN_CHAT_ID=431292182,190545165
ADMIN_IDS=431292182,190545165
CHANNEL_ID=-1001234567890
CHANNEL_USERNAME=@your_channel_username
CHANNEL_INVITE_LINK=https://t.me/+gstVWYW2Kgo2OGYy

# Prodamus Configuration
PRODAMUS_SHOP_ID=dashastar
PRODAMUS_SECRET_KEY=b2f9e8a399225271521dfe88a277a7371cb8c2cebfeaa6f0276ba81fcc303c93
PRODAMUS_DEMO_MODE=true
PRODAMUS_WEBHOOK_URL=http://82.147.71.244:5000/sales/prodamus

# Webhook Configuration
WEBHOOK_URL=http://82.147.71.244:5000/webhook/telegram
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
DEBUG=false

# Smart Sender Configuration
SMART_SENDER_API_KEY=your_smart_sender_api_key_here
EOF

echo "✅ .env файл обновлен для использования IP"

# 3. Проверка конфигурации
echo "🔍 Проверка конфигурации..."
echo "   - PRODAMUS_WEBHOOK_URL: $(grep PRODAMUS_WEBHOOK_URL .env)"
echo "   - WEBHOOK_URL: $(grep WEBHOOK_URL .env)"

# 4. Запуск webhook сервера
echo "🚀 Запуск webhook сервера..."
python3 webhook.py &
WEBHOOK_PID=$!
sleep 3

# 5. Проверка webhook
echo "🧪 Проверка webhook сервера..."
curl -s http://localhost:5000/health

if [ $? -eq 0 ]; then
    echo "   ✅ Webhook сервер запущен (PID: $WEBHOOK_PID)"
else
    echo "   ❌ Ошибка запуска webhook сервера"
    exit 1
fi

# 6. Проверка доступности по IP
echo "🧪 Проверка доступности по IP..."
curl -s http://82.147.71.244:5000/health

if [ $? -eq 0 ]; then
    echo "   ✅ Webhook доступен по IP"
else
    echo "   ❌ Webhook недоступен по IP"
    echo "   🔧 Проверьте настройки файрвола и портов"
fi

echo ""
echo "🎉 IP WEBHOOK НАСТРОЕН!"
echo ""
echo "📝 Статус:"
echo "   - Webhook PID: $WEBHOOK_PID"
echo "   - Локальный URL: http://localhost:5000"
echo "   - Внешний URL: http://82.147.71.244:5000"
echo ""
echo "🧪 Тестирование:"
echo "   python3 test_full_payment_flow.py"
echo "   python3 check_webhook_status.py"
echo ""
echo "⚠️ ВНИМАНИЕ: Используется IP адрес вместо PageKite!"
echo "🔧 Это временное решение для тестирования"
echo "📋 После тестирования нужно будет настроить PageKite"
