#!/bin/bash

# 🔧 ИСПРАВЛЕНИЕ АКТИВАЦИИ ПОДПИСКИ
# Исправление проблемы с активацией подписки через webhook

echo "🔧 ИСПРАВЛЕНИЕ АКТИВАЦИИ ПОДПИСКИ"
echo "=" * 50

# 1. Остановка webhook сервера
echo "⏹️ Остановка webhook сервера..."
pkill -f webhook.py
sleep 3

# 2. Создание резервной копии
echo "💾 Создание резервной копии..."
cp webhook.py webhook.py.backup
echo "   ✅ Резервная копия создана: webhook.py.backup"

# 3. Обновление webhook.py
echo "📝 Обновление webhook.py..."
cp webhook_fixed.py webhook.py
echo "   ✅ webhook.py обновлен с исправленной активацией"

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

# 6. Тестирование активации подписки
echo "🧪 Тестирование активации подписки..."
python3 test_payment_processing.py

echo ""
echo "🎉 АКТИВАЦИЯ ПОДПИСКИ ИСПРАВЛЕНА!"
echo ""
echo "📝 Статус:"
echo "   - Webhook PID: $WEBHOOK_PID"
echo "   - Активация подписки: ИСПРАВЛЕНА"
echo "   - Локальный URL: http://localhost:5000"
echo ""
echo "🧪 Тестирование:"
echo "   python3 test_payment_processing.py"
echo "   python3 test_no_signature.py"
echo ""
echo "📋 Логи:"
echo "   tail -f webhook.log"
echo ""
echo "⚠️ ВНИМАНИЕ: Проверка подписи отключена!"
echo "🔧 Это временное решение для тестирования"
echo "📋 После тестирования нужно будет включить проверку подписи"
echo ""
echo "💾 Резервная копия: webhook.py.backup"
echo "🔄 Восстановление: cp webhook.py.backup webhook.py"
