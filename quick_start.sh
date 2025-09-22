#!/bin/bash

# 🚀 БЫСТРЫЙ ЗАПУСК БОТА
# Простой запуск бота с webhook

echo "🚀 БЫСТРЫЙ ЗАПУСК БОТА"
echo "=" * 50

# 1. Остановка старых процессов
echo "⏹️ Остановка старых процессов..."
pkill -f webhook.py
pkill -f pagekite.py
pkill -f main.py
pkill -f main_with_webhook.py
sleep 2

# 2. Запуск бота с webhook
echo "🤖 Запуск бота с webhook..."
python3 main_with_webhook.py &
BOT_PID=$!

# 3. Запуск PageKite
echo "🌐 Запуск PageKite..."
./pagekite.py 5000 dashastar.pagekite.me &
PAGKITE_PID=$!

# 4. Ожидание запуска
echo "⏳ Ожидание запуска..."
sleep 10

# 5. Проверка статуса
echo "🔍 Проверка статуса..."
echo "   - Bot PID: $BOT_PID"
echo "   - PageKite PID: $PAGKITE_PID"
echo "   - Локальный health: $(curl -s http://localhost:5000/health)"
echo "   - Удаленный health: $(curl -s https://dashastar.pagekite.me/health)"

echo ""
echo "🎉 БОТ ЗАПУЩЕН!"
echo ""
echo "📝 Статус:"
echo "   - Bot: запущен"
echo "   - Webhook: запущен"
echo "   - PageKite: запущен"
echo ""
echo "🧪 Тестирование:"
echo "   python3 test_no_signature.py"
echo ""
echo "🛑 Остановка:"
echo "   ./stop_bot_with_webhook.sh"
