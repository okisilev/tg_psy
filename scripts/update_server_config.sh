#!/bin/bash

# 🔧 СКРИПТ ОБНОВЛЕНИЯ КОНФИГУРАЦИИ НА СЕРВЕРЕ
# Использование: ./update_server_config.sh

echo "🔧 ОБНОВЛЕНИЕ КОНФИГУРАЦИИ НА СЕРВЕРЕ"
echo "=" * 60

# 1. Остановка webhook сервера
echo "⏹️ Остановка webhook сервера..."
pkill -f webhook_http.py
sleep 2

# 2. Обновление переменных окружения
echo "⚙️ Обновление переменных окружения..."
export FLASK_PORT="5000"
export PRODAMUS_WEBHOOK_URL="http://82.147.71.244:5000/sales/prodamus"
export WEBHOOK_URL="http://82.147.71.244:5000/webhook/telegram"

echo "✅ Переменные окружения обновлены:"
echo "   - FLASK_PORT: $FLASK_PORT"
echo "   - PRODAMUS_WEBHOOK_URL: $PRODAMUS_WEBHOOK_URL"
echo "   - WEBHOOK_URL: $WEBHOOK_URL"

# 3. Создание .env файла
echo "📝 Создание .env файла..."
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
EOF

echo "✅ .env файл создан"

# 4. Проверка конфигурации
echo "🔍 Проверка конфигурации..."
python3 check_config.py

# 5. Запуск webhook сервера
echo "🚀 Запуск webhook сервера..."
python3 webhook_http.py &

# 6. Ожидание запуска
echo "⏳ Ожидание запуска сервера..."
sleep 3

# 7. Проверка работы
echo "🧪 Проверка работы webhook..."
curl -s http://localhost:5000/health

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Webhook сервер запущен успешно!"
    echo ""
    echo "📝 Настройки для Prodamus:"
    echo "   - Webhook URL: http://82.147.71.244:5000/sales/prodamus"
    echo "   - Метод: POST"
    echo "   - Заголовки: Sign: {signature}"
    echo ""
    echo "🧪 Тест webhook:"
    echo "   curl -X POST http://82.147.71.244:5000/sales/prodamus \\"
    echo "     -H 'Content-Type: application/json' \\"
    echo "     -H 'Sign: 919cb318867507f7e48790c3c2c2435f54bd62a29b8e7bd32157840bf546bb34' \\"
    echo "     -d '{\"order_id\":\"women_club_431292182_test\",\"sum\":\"50.00\",\"currency\":\"rub\",\"payment_status\":\"success\"}'"
else
    echo "❌ Ошибка запуска webhook сервера"
    exit 1
fi

echo ""
echo "🎉 Конфигурация обновлена!"
echo "✅ Webhook готов к работе на порту 5000"
