#!/bin/bash

# 🚀 ЗАПУСК БОТА С WEBHOOK
# Запуск бота с webhook сервером и PageKite

echo "🚀 ЗАПУСК БОТА С WEBHOOK"
echo "=" * 50

# 1. Остановка всех процессов
echo "⏹️ Остановка всех процессов..."
pkill -f webhook.py
pkill -f pagekite.py
pkill -f main.py
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

# 3. Запуск webhook сервера
echo "🚀 Запуск webhook сервера..."
python3 webhook.py &
WEBHOOK_PID=$!
sleep 3

# 4. Проверка webhook
echo "🧪 Проверка webhook сервера..."
WEBHOOK_STATUS=$(curl -s http://localhost:5000/health | grep -o '"status":"ok"' | wc -l)
if [ $WEBHOOK_STATUS -gt 0 ]; then
    echo "   ✅ Webhook сервер запущен (PID: $WEBHOOK_PID)"
else
    echo "   ❌ Ошибка запуска webhook сервера"
    echo "   📋 Логи webhook:"
    tail -20 webhook.log 2>/dev/null || echo "   Логи не найдены"
    exit 1
fi

# 5. Запуск PageKite
echo "🌐 Запуск PageKite..."
./pagekite.py 5000 dashastar.pagekite.me &
PAGKITE_PID=$!
sleep 10

# 6. Проверка PageKite
echo "🧪 Проверка PageKite..."
PAGKITE_STATUS=$(curl -s https://dashastar.pagekite.me/health | grep -o '"status":"ok"' | wc -l)
if [ $PAGKITE_STATUS -gt 0 ]; then
    echo "   ✅ PageKite работает (PID: $PAGKITE_PID)"
else
    echo "   ❌ PageKite не работает"
    echo "   📋 Логи PageKite:"
    tail -20 pagekite.log 2>/dev/null || echo "   Логи не найдены"
    echo "   🔧 Попробуем альтернативный запуск..."
    
    # Альтернативный запуск PageKite
    nohup ./pagekite.py 5000 dashastar.pagekite.me --frontend > pagekite.log 2>&1 &
    PAGKITE_PID=$!
    sleep 10
    
    PAGKITE_STATUS=$(curl -s https://dashastar.pagekite.me/health | grep -o '"status":"ok"' | wc -l)
    if [ $PAGKITE_STATUS -gt 0 ]; then
        echo "   ✅ PageKite работает после альтернативного запуска"
    else
        echo "   ❌ PageKite все еще не работает"
        echo "   📋 Проверьте логи: tail -f pagekite.log"
    fi
fi

# 7. Запуск бота с webhook
echo "🤖 Запуск бота с webhook..."
python3 main_with_webhook.py &
BOT_PID=$!
sleep 5

# 8. Проверка бота
echo "🧪 Проверка бота..."
BOT_STATUS=$(ps aux | grep main_with_webhook.py | grep -v grep | wc -l)
if [ $BOT_STATUS -gt 0 ]; then
    echo "   ✅ Бот с webhook запущен (PID: $BOT_PID)"
else
    echo "   ❌ Ошибка запуска бота"
    echo "   📋 Логи бота:"
    tail -20 bot.log 2>/dev/null || echo "   Логи не найдены"
fi

# 9. Финальная проверка
echo ""
echo "🧪 Финальная проверка:"
echo "   - Локальный health: $(curl -s http://localhost:5000/health)"
echo "   - Удаленный health: $(curl -s https://dashastar.pagekite.me/health)"

# 10. Проверка процессов
echo ""
echo "🔍 Финальная проверка процессов:"
ps aux | grep -E "(webhook|pagekite|main)" | grep -v grep

echo ""
echo "🎉 БОТ С WEBHOOK ЗАПУЩЕН!"
echo ""
echo "📝 Статус:"
echo "   - Webhook PID: $WEBHOOK_PID"
echo "   - PageKite PID: $PAGKITE_PID"
echo "   - Bot PID: $BOT_PID"
echo "   - Локальный URL: http://localhost:5000"
echo "   - Удаленный URL: https://dashastar.pagekite.me"
echo ""
echo "🧪 Тестирование:"
echo "   python3 test_no_signature.py"
echo "   python3 test_full_payment_flow.py"
echo ""
echo "📋 Логи:"
echo "   - Бот: tail -f bot.log"
echo "   - Webhook: tail -f webhook.log"
echo "   - PageKite: tail -f pagekite.log"
echo ""
echo "🛑 Остановка:"
echo "   ./stop_bot_with_webhook.sh"
