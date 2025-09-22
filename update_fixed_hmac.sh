#!/bin/bash

# 🔧 ОБНОВЛЕНИЕ С ИСПРАВЛЕННОЙ БИБЛИОТЕКОЙ HMAC
# Обновление prodamus.py с исправленной библиотекой Hmac

echo "🔧 ОБНОВЛЕНИЕ С ИСПРАВЛЕННОЙ БИБЛИОТЕКОЙ HMAC"
echo "=" * 50

# 1. Остановка webhook сервера
echo "⏹️ Остановка webhook сервера..."
pkill -f webhook.py
sleep 3

# 2. Замена prodamus.py на исправленную версию
echo "📝 Замена prodamus.py на исправленную версию..."
cp prodamus_fixed.py prodamus.py

echo "✅ prodamus.py обновлен с исправленной библиотекой Hmac"

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
echo "🎉 ИСПРАВЛЕННАЯ БИБЛИОТЕКА HMAC ОБНОВЛЕНА!"
echo ""
echo "📝 Статус:"
echo "   - Webhook PID: $WEBHOOK_PID"
echo "   - PageKite PID: $PAGKITE_PID"
echo "   - Локальный URL: http://localhost:5000"
echo "   - Удаленный URL: https://dashastar.pagekite.me"
echo ""
echo "🧪 Тестирование:"
echo "   python3 test_official_hmac.py"
echo "   python3 check_webhook_status.py"
echo ""
echo "📋 Теперь используется исправленная библиотека Hmac с 10 вариантами!"
echo "🔧 Это должно найти правильный алгоритм Prodamus!"
