#!/bin/bash

# 🚀 ЗАПУСК PAGKITE И WEBHOOK СЕРВЕРА
# Запуск webhook сервера с PageKite туннелем

echo "🚀 ЗАПУСК PAGKITE И WEBHOOK СЕРВЕРА"
echo "=" * 50

# 1. Остановка старых процессов
echo "⏹️ Остановка старых процессов..."
pkill -f webhook_http.py
pkill -f pagekite.py
sleep 2

# 2. Установка переменных окружения
echo "⚙️ Установка переменных окружения..."
export FLASK_PORT="5000"
export PRODAMUS_WEBHOOK_URL="https://dashastar.pagekite.me/sales/prodamus"
export WEBHOOK_URL="https://dashastar.pagekite.me/webhook/telegram"

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
PRODAMUS_WEBHOOK_URL=https://dashastar.pagekite.me/sales/prodamus
WEBHOOK_URL=https://dashastar.pagekite.me/webhook/telegram
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
DEBUG=false
EOF

echo "✅ .env файл создан"

# 4. Запуск webhook сервера
echo "🚀 Запуск webhook сервера..."
python3 webhook_http.py &
WEBHOOK_PID=$!

# 5. Ожидание запуска webhook
echo "⏳ Ожидание запуска webhook сервера..."
sleep 3

# 6. Проверка webhook
echo "🧪 Проверка webhook сервера..."
curl -s http://localhost:5000/health

if [ $? -eq 0 ]; then
    echo "   ✅ Webhook сервер запущен (PID: $WEBHOOK_PID)"
else
    echo "   ❌ Ошибка запуска webhook сервера"
    exit 1
fi

# 7. Запуск PageKite
echo "🌐 Запуск PageKite..."
pagekite.py 5000 dashastar.pagekite.me &
PAGKITE_PID=$!

# 8. Ожидание запуска PageKite
echo "⏳ Ожидание запуска PageKite..."
sleep 5

# 9. Проверка PageKite
echo "🧪 Проверка PageKite..."
curl -s https://dashastar.pagekite.me/health

if [ $? -eq 0 ]; then
    echo "   ✅ PageKite работает (PID: $PAGKITE_PID)"
    echo ""
    echo "🎉 PAGKITE И WEBHOOK ЗАПУЩЕНЫ!"
    echo ""
    echo "📝 Настройки для Prodamus:"
    echo "   - Webhook URL: https://dashastar.pagekite.me/sales/prodamus"
    echo "   - Метод: POST"
    echo "   - Заголовки: Sign: {signature}"
    echo ""
    echo "📝 Настройки для Telegram:"
    echo "   - Webhook URL: https://dashastar.pagekite.me/webhook/telegram"
    echo "   - Метод: POST"
    echo ""
    echo "🧪 Тест webhook:"
    echo "   curl -X POST https://dashastar.pagekite.me/sales/prodamus \\"
    echo "     -H 'Content-Type: application/json' \\"
    echo "     -H 'Sign: 30ba444dc24a268bdb78669632c6e0777652c0e63217b6cbc9adcb5fb2a0adaa' \\"
    echo "     -d '{\"order_id\":\"women_club_431292182_test\",\"sum\":\"50.00\",\"currency\":\"rub\",\"payment_status\":\"success\"}'"
    echo ""
    echo "🔧 Управление процессами:"
    echo "   - Webhook PID: $WEBHOOK_PID"
    echo "   - PageKite PID: $PAGKITE_PID"
    echo "   - Остановка: kill $WEBHOOK_PID $PAGKITE_PID"
else
    echo "   ❌ PageKite не работает"
    echo "   🔧 Проверьте настройки PageKite"
fi

echo ""
echo "✅ СЕРВИСЫ ЗАПУЩЕНЫ!"
echo "🌐 Webhook доступен по адресу: https://dashastar.pagekite.me"
