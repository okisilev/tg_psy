#!/bin/bash

# 🔧 ВРЕМЕННОЕ ОТКЛЮЧЕНИЕ ПРОВЕРКИ ПОДПИСИ
# Отключение проверки подписи для тестирования webhook

echo "🔧 ВРЕМЕННОЕ ОТКЛЮЧЕНИЕ ПРОВЕРКИ ПОДПИСИ"
echo "=" * 50

# 1. Остановка webhook сервера
echo "⏹️ Остановка webhook сервера..."
pkill -f webhook.py
sleep 3

# 2. Замена prodamus.py на версию без проверки подписи
echo "📝 Замена prodamus.py на версию без проверки подписи..."
cp prodamus_no_signature.py prodamus.py

echo "✅ prodamus.py обновлен БЕЗ проверки подписи (тестовый режим)"

# 3. Запуск webhook сервера
echo "🚀 Запуск webhook сервера..."
python3 webhook.py &
WEBHOOK_PID=$!
sleep 3

# 4. Проверка webhook
echo "🧪 Проверка webhook сервера..."
curl -s http://localhost:5000/health

if [ $? -eq 0 ]; then
    echo "   ✅ Webhook сервер запущен (PID: $WEBHOOK_PID)"
else
    echo "   ❌ Ошибка запуска webhook сервера"
    exit 1
fi

# 5. Запуск PageKite
echo "🌐 Запуск PageKite..."
./pagekite.py 5000 dashastar.pagekite.me &
PAGKITE_PID=$!
sleep 10

# 6. Проверка PageKite
echo "🧪 Проверка PageKite..."
curl -s https://dashastar.pagekite.me/health

if [ $? -eq 0 ]; then
    echo "   ✅ PageKite работает (PID: $PAGKITE_PID)"
else
    echo "   ❌ PageKite не работает"
fi

echo ""
echo "🎉 ПРОВЕРКА ПОДПИСИ ВРЕМЕННО ОТКЛЮЧЕНА!"
echo ""
echo "📝 Статус:"
echo "   - Webhook PID: $WEBHOOK_PID"
echo "   - PageKite PID: $PAGKITE_PID"
echo "   - Локальный URL: http://localhost:5000"
echo "   - Удаленный URL: https://dashastar.pagekite.me"
echo ""
echo "🧪 Тестирование:"
echo "   python3 test_fixed_hmac.py"
echo "   python3 check_webhook_status.py"
echo ""
echo "⚠️ ВНИМАНИЕ: Проверка подписи отключена для тестирования!"
echo "🔧 Теперь webhook должен принимать все запросы от Prodamus"
echo "📋 После тестирования нужно будет включить проверку подписи обратно"
