#!/bin/bash

# 🛑 ОСТАНОВКА БОТА С WEBHOOK
# Остановка бота, webhook сервера и PageKite

echo "🛑 ОСТАНОВКА БОТА С WEBHOOK"
echo "=" * 50

# 1. Остановка всех процессов
echo "⏹️ Остановка всех процессов..."
pkill -f webhook.py
pkill -f pagekite.py
pkill -f main.py
pkill -f main_with_webhook.py
sleep 3

# 2. Проверка остановки
echo "🔍 Проверка остановки..."
REMAINING_PROCESSES=$(ps aux | grep -E "(webhook|pagekite|main)" | grep -v grep | wc -l)
if [ $REMAINING_PROCESSES -gt 0 ]; then
    echo "   ⚠️ Остались процессы:"
    ps aux | grep -E "(webhook|pagekite|main)" | grep -v grep
    echo "   🔧 Принудительная остановка..."
    pkill -9 -f webhook.py
    pkill -9 -f pagekite.py
    pkill -9 -f main.py
    sleep 3
fi

# 3. Финальная проверка
echo "🔍 Финальная проверка..."
REMAINING_PROCESSES=$(ps aux | grep -E "(webhook|pagekite|main)" | grep -v grep | wc -l)
if [ $REMAINING_PROCESSES -eq 0 ]; then
    echo "   ✅ Все процессы остановлены"
else
    echo "   ❌ Остались процессы:"
    ps aux | grep -E "(webhook|pagekite|main)" | grep -v grep
fi

echo ""
echo "🎉 БОТ С WEBHOOK ОСТАНОВЛЕН!"
echo ""
echo "📝 Статус:"
echo "   - Webhook: остановлен"
echo "   - PageKite: остановлен"
echo "   - Bot: остановлен"
echo ""
echo "🚀 Запуск:"
echo "   ./start_bot_with_webhook.sh"
