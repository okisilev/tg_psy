#!/bin/bash

# 🚀 БЫСТРОЕ ИСПРАВЛЕНИЕ PAGKITE И WEBHOOK
# Простое исправление проблем

echo "🚀 БЫСТРОЕ ИСПРАВЛЕНИЕ PAGKITE И WEBHOOK"
echo "=" * 50

# 1. Остановка всех процессов
echo "⏹️ Остановка всех процессов..."
pkill -f webhook.py
pkill -f pagekite.py
pkill -f main.py
sleep 3

# 2. Запуск webhook сервера
echo "🚀 Запуск webhook сервера..."
python3 webhook.py &
WEBHOOK_PID=$!
sleep 3

# 3. Проверка webhook
echo "🧪 Проверка webhook..."
curl -s http://localhost:5000/health
echo ""

# 4. Запуск PageKite
echo "🌐 Запуск PageKite..."
./pagekite.py 5000 dashastar.pagekite.me &
PAGKITE_PID=$!
sleep 10

# 5. Проверка PageKite
echo "🧪 Проверка PageKite..."
curl -s https://dashastar.pagekite.me/health
echo ""

# 6. Статус
echo "📝 Статус:"
echo "   - Webhook PID: $WEBHOOK_PID"
echo "   - PageKite PID: $PAGKITE_PID"
echo "   - Локальный: http://localhost:5000"
echo "   - Удаленный: https://dashastar.pagekite.me"

echo ""
echo "✅ БЫСТРОЕ ИСПРАВЛЕНИЕ ЗАВЕРШЕНО!"
echo ""
echo "🧪 Тестирование:"
echo "   python3 check_webhook_status.py"
echo "   python3 test_post_webhook.py"
