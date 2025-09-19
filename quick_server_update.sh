#!/bin/bash

# 🚀 БЫСТРОЕ ОБНОВЛЕНИЕ КОНФИГУРАЦИИ НА СЕРВЕРЕ

echo "🚀 БЫСТРОЕ ОБНОВЛЕНИЕ КОНФИГУРАЦИИ"
echo "=" * 50

# 1. Остановка старых процессов
echo "⏹️ Остановка старых процессов..."
pkill -f webhook_http.py
sleep 2

# 2. Установка переменных окружения
echo "⚙️ Установка переменных окружения..."
export FLASK_PORT="5000"
export PRODAMUS_WEBHOOK_URL="http://82.147.71.244:5000/sales/prodamus"
export WEBHOOK_URL="http://82.147.71.244:5000/webhook/telegram"

# 3. Создание .env файла
echo "📝 Создание .env файла..."
cat > .env << 'EOF'
BOT_TOKEN=8455794146:AAFf9DEcTxLnJfG-HWWmzwpSjTRDzNE3px8
ADMIN_CHAT_ID=431292182,190545165
ADMIN_IDS=431292182,190545165
CHANNEL_ID=-1001234567890
CHANNEL_USERNAME=@your_channel_username
CHANNEL_INVITE_LINK=https://t.me/+gstVWYW2Kgo2OGYy
PRODAMUS_SHOP_ID=dashastar
PRODAMUS_SECRET_KEY=b2f9e8a399225271521dfe88a277a7371cb8c2cebfeaa6f0276ba81fcc303c93
PRODAMUS_DEMO_MODE=true
PRODAMUS_WEBHOOK_URL=http://82.147.71.244:5000/sales/prodamus
WEBHOOK_URL=http://82.147.71.244:5000/webhook/telegram
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
DEBUG=false
EOF

# 4. Запуск webhook сервера
echo "🚀 Запуск webhook сервера на порту 5000..."
python3 webhook_http.py &

# 5. Ожидание запуска
echo "⏳ Ожидание запуска..."
sleep 3

# 6. Проверка работы
echo "🧪 Проверка работы..."
curl -s http://localhost:5000/health

echo ""
echo "✅ ГОТОВО!"
echo ""
echo "📝 Настройки для Prodamus:"
echo "   Webhook URL: http://82.147.71.244:5000/sales/prodamus"
echo "   Метод: POST"
echo "   Заголовки: Sign: {signature}"
echo ""
echo "🧪 Тест:"
echo "   curl -X POST http://82.147.71.244:5000/sales/prodamus \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -H 'Sign: 919cb318867507f7e48790c3c2c2435f54bd62a29b8e7bd32157840bf546bb34' \\"
echo "     -d '{\"order_id\":\"women_club_431292182_test\",\"sum\":\"50.00\",\"currency\":\"rub\",\"payment_status\":\"success\"}'"
