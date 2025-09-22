#!/bin/bash

# 🔧 ИСПРАВЛЕНИЕ WEBHOOK URLS
# Обновление URL для использования PageKite вместо IP

echo "🔧 ИСПРАВЛЕНИЕ WEBHOOK URLS"
echo "=" * 50

# 1. Остановка webhook сервера
echo "⏹️ Остановка webhook сервера..."
pkill -f webhook.py
sleep 3

# 2. Обновление .env файла
echo "📝 Обновление .env файла..."
cp .env_new .env

echo "✅ .env файл обновлен с PageKite URLs"

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

# 6. Запуск PageKite
echo "🌐 Запуск PageKite..."
./pagekite.py 5000 dashastar.pagekite.me &
PAGKITE_PID=$!
sleep 10

# 7. Проверка PageKite
echo "🧪 Проверка PageKite..."
curl -s https://dashastar.pagekite.me/health

if [ $? -eq 0 ]; then
    echo "   ✅ PageKite работает (PID: $PAGKITE_PID)"
else
    echo "   ❌ PageKite не работает"
fi

echo ""
echo "🎉 WEBHOOK URLS ИСПРАВЛЕНЫ!"
echo ""
echo "📝 Статус:"
echo "   - Webhook PID: $WEBHOOK_PID"
echo "   - PageKite PID: $PAGKITE_PID"
echo "   - Локальный URL: http://localhost:5000"
echo "   - Удаленный URL: https://dashastar.pagekite.me"
echo ""
echo "🧪 Тестирование:"
echo "   python3 test_full_payment_flow.py"
echo "   python3 check_webhook_status.py"
echo ""
echo "📋 Теперь webhook использует PageKite URLs!"
echo "🔧 Prodamus будет отправлять уведомления на правильный адрес"
