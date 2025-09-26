#!/bin/bash

# 🔄 ПЕРЕЗАПУСК WEBHOOK СЕРВЕРА
# Перезапуск webhook сервера для исправления проблем

echo "🔄 ПЕРЕЗАПУСК WEBHOOK СЕРВЕРА"
echo "=" * 50

# 1. Остановка всех процессов
echo "⏹️ Остановка всех процессов..."
pkill -f webhook.py
pkill -f webhook_http.py
pkill -f pagekite.py
pkill -f main.py
sleep 3

# 2. Проверка остановки процессов
echo "🔍 Проверка остановки процессов..."
WEBHOOK_PROCESSES=$(ps aux | grep -E "(webhook|pagekite|main)" | grep -v grep | wc -l)
if [ $WEBHOOK_PROCESSES -eq 0 ]; then
    echo "   ✅ Все процессы остановлены"
else
    echo "   ⚠️ Некоторые процессы все еще работают"
    ps aux | grep -E "(webhook|pagekite|main)" | grep -v grep
fi

# 3. Обновление переменных окружения
echo "⚙️ Обновление переменных окружения..."
export FLASK_PORT="5000"
export PRODAMUS_WEBHOOK_URL="https://dashastar.pagekite.me/sales/prodamus"
export WEBHOOK_URL="https://dashastar.pagekite.me/webhook/telegram"

echo "✅ Переменные окружения обновлены"

# 4. Создание .env файла
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

# 5. Запуск webhook сервера
echo "🚀 Запуск webhook сервера..."
python3 webhook.py &
WEBHOOK_PID=$!

# 6. Ожидание запуска webhook
echo "⏳ Ожидание запуска webhook сервера..."
sleep 3

# 7. Проверка webhook
echo "🧪 Проверка webhook сервера..."
curl -s http://localhost:5000/health

if [ $? -eq 0 ]; then
    echo "   ✅ Webhook сервер запущен (PID: $WEBHOOK_PID)"
else
    echo "   ❌ Ошибка запуска webhook сервера"
    exit 1
fi

# 8. Запуск PageKite
echo "🌐 Запуск PageKite..."
./pagekite.py 5000 dashastar.pagekite.me &
PAGKITE_PID=$!

# 9. Ожидание запуска PageKite
echo "⏳ Ожидание запуска PageKite..."
sleep 5

# 10. Проверка PageKite
echo "🧪 Проверка PageKite..."
curl -s https://dashastar.pagekite.me/health

if [ $? -eq 0 ]; then
    echo "   ✅ PageKite работает (PID: $PAGKITE_PID)"
    echo ""
    echo "🎉 WEBHOOK И PAGKITE ПЕРЕЗАПУЩЕНЫ!"
    echo ""
    echo "📝 Настройки для Prodamus:"
    echo "   - Webhook URL: https://dashastar.pagekite.me/sales/prodamus"
    echo "   - Метод: POST"
    echo "   - Заголовки: Sign: {signature}"
    echo ""
    echo "🧪 Тест webhook:"
    echo "   python3 check_webhook_status.py"
    echo ""
    echo "🔧 Управление:"
    echo "   - Webhook PID: $WEBHOOK_PID"
    echo "   - PageKite PID: $PAGKITE_PID"
    echo "   - Остановка: kill $WEBHOOK_PID $PAGKITE_PID"
else
    echo "   ❌ PageKite не работает"
    echo "   🔧 Проверьте настройки PageKite"
fi

echo ""
echo "✅ СЕРВИСЫ ПЕРЕЗАПУЩЕНЫ!"
echo "🌐 Webhook доступен по адресу: https://dashastar.pagekite.me"
