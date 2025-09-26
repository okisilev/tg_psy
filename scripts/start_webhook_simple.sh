#!/bin/bash

# 🚀 ПРОСТОЙ ЗАПУСК WEBHOOK СЕРВЕРА
# Запуск webhook сервера без PageKite (для тестирования)

echo "🚀 ПРОСТОЙ ЗАПУСК WEBHOOK СЕРВЕРА"
echo "=" * 50

# 1. Остановка старых процессов
echo "⏹️ Остановка старых процессов..."
pkill -f webhook_http.py
pkill -f pagekite.py
sleep 2

# 2. Установка переменных окружения
echo "⚙️ Установка переменных окружения..."
export FLASK_PORT="5000"
export PRODAMUS_WEBHOOK_URL="http://82.147.71.244:5000/sales/prodamus"
export WEBHOOK_URL="http://82.147.71.244:5000/webhook/telegram"

echo "✅ Переменные окружения установлены"

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

echo "✅ .env файл создан"

# 4. Запуск webhook сервера
echo "🚀 Запуск webhook сервера..."
python3 webhook_http.py &
WEBHOOK_PID=$!

# 5. Ожидание запуска
echo "⏳ Ожидание запуска webhook сервера..."
sleep 3

# 6. Проверка работы
echo "🧪 Проверка работы webhook сервера..."
curl -s http://localhost:5000/health

if [ $? -eq 0 ]; then
    echo "   ✅ Webhook сервер запущен (PID: $WEBHOOK_PID)"
    echo ""
    echo "🎉 WEBHOOK СЕРВЕР ЗАПУЩЕН!"
    echo ""
    echo "📝 Настройки для Prodamus:"
    echo "   - Webhook URL: http://82.147.71.244:5000/sales/prodamus"
    echo "   - Метод: POST"
    echo "   - Заголовки: Sign: {signature}"
    echo ""
    echo "📝 Настройки для Telegram:"
    echo "   - Webhook URL: http://82.147.71.244:5000/webhook/telegram"
    echo "   - Метод: POST"
    echo ""
    echo "🧪 Тест webhook:"
    echo "   curl -X POST http://82.147.71.244:5000/sales/prodamus \\"
    echo "     -H 'Content-Type: application/json' \\"
    echo "     -H 'Sign: 30ba444dc24a268bdb78669632c6e0777652c0e63217b6cbc9adcb5fb2a0adaa' \\"
    echo "     -d '{\"order_id\":\"women_club_431292182_test\",\"sum\":\"50.00\",\"currency\":\"rub\",\"payment_status\":\"success\"}'"
    echo ""
    echo "🔧 Управление:"
    echo "   - PID: $WEBHOOK_PID"
    echo "   - Остановка: kill $WEBHOOK_PID"
    echo "   - Проверка: curl http://localhost:5000/health"
else
    echo "   ❌ Ошибка запуска webhook сервера"
    exit 1
fi

echo ""
echo "✅ WEBHOOK СЕРВЕР ЗАПУЩЕН!"
echo "🌐 Доступен по адресу: http://82.147.71.244:5000"
