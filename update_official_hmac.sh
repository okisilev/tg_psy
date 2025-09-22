#!/bin/bash

# 🔧 ОБНОВЛЕНИЕ С ОФИЦИАЛЬНОЙ БИБЛИОТЕКОЙ HMAC
# Обновление prodamus.py с официальной библиотекой Hmac от Prodamus

echo "🔧 ОБНОВЛЕНИЕ С ОФИЦИАЛЬНОЙ БИБЛИОТЕКОЙ HMAC"
echo "=" * 50

# 1. Остановка webhook сервера
echo "⏹️ Остановка webhook сервера..."
pkill -f webhook.py
sleep 3

# 2. Замена prodamus.py на официальную версию
echo "📝 Замена prodamus.py на официальную версию..."
cp prodamus_official.py prodamus.py

echo "✅ prodamus.py обновлен с официальной библиотекой Hmac"

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
echo "🎉 ОФИЦИАЛЬНАЯ БИБЛИОТЕКА HMAC ОБНОВЛЕНА!"
echo ""
echo "📝 Статус:"
echo "   - Webhook PID: $WEBHOOK_PID"
echo "   - PageKite PID: $PAGKITE_PID"
echo "   - Локальный URL: http://localhost:5000"
echo "   - Удаленный URL: https://dashastar.pagekite.me"
echo ""
echo "🧪 Тестирование:"
echo "   python3 test_correct_signature.py"
echo "   python3 check_webhook_status.py"
echo ""
echo "📋 Теперь используется официальная библиотека Hmac от Prodamus!"
echo "🔧 Это должно решить проблему с подписью webhook!"
echo ""
echo "📚 Основано на документации:"
echo "   https://help.prodamus.ru/payform/integracii/rest-api/instrukcii-dlya-samostoyatelnaya-integracii-servisov"
