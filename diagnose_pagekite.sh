#!/bin/bash

# 🔍 ДИАГНОСТИКА PAGKITE
# Диагностика и исправление проблемы с PageKite

echo "🔍 ДИАГНОСТИКА PAGKITE"
echo "=" * 50

# 1. Проверка процессов
echo "📋 Проверка процессов:"
echo "   - Webhook процессы:"
ps aux | grep webhook | grep -v grep
echo "   - PageKite процессы:"
ps aux | grep pagekite | grep -v grep
echo ""

# 2. Проверка портов
echo "📋 Проверка портов:"
echo "   - Порт 5000:"
netstat -tlnp | grep :5000
echo ""

# 3. Проверка локального webhook
echo "📋 Проверка локального webhook:"
curl -s http://localhost:5000/health
echo ""
echo ""

# 4. Проверка PageKite
echo "📋 Проверка PageKite:"
curl -s https://dashastar.pagekite.me/health
echo ""
echo ""

# 5. Остановка всех процессов
echo "⏹️ Остановка всех процессов..."
pkill -f webhook.py
pkill -f pagekite.py
pkill -f main.py
sleep 5

# 6. Проверка остановки
echo "🔍 Проверка остановки:"
REMAINING_PROCESSES=$(ps aux | grep -E "(webhook|pagekite|main)" | grep -v grep | wc -l)
if [ $REMAINING_PROCESSES -eq 0 ]; then
    echo "   ✅ Все процессы остановлены"
else
    echo "   ⚠️ Остались процессы:"
    ps aux | grep -E "(webhook|pagekite|main)" | grep -v grep
    echo "   🔧 Принудительная остановка..."
    pkill -9 -f webhook.py
    pkill -9 -f pagekite.py
    pkill -9 -f main.py
    sleep 3
fi

# 7. Запуск webhook сервера
echo "🚀 Запуск webhook сервера..."
python3 webhook.py &
WEBHOOK_PID=$!
sleep 3

# 8. Проверка webhook
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

# 9. Запуск PageKite
echo "🌐 Запуск PageKite..."
./pagekite.py 5000 dashastar.pagekite.me &
PAGKITE_PID=$!
sleep 10

# 10. Проверка PageKite
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

# 11. Финальная проверка
echo ""
echo "🧪 Финальная проверка:"
echo "   - Локальный health: $(curl -s http://localhost:5000/health)"
echo "   - Удаленный health: $(curl -s https://dashastar.pagekite.me/health)"

# 12. Проверка процессов
echo ""
echo "🔍 Финальная проверка процессов:"
ps aux | grep -E "(webhook|pagekite)" | grep -v grep

echo ""
echo "🎉 ДИАГНОСТИКА ЗАВЕРШЕНА!"
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
echo "📋 Если PageKite не работает:"
echo "   1. Проверьте интернет соединение"
echo "   2. Проверьте логи: tail -f pagekite.log"
echo "   3. Попробуйте перезапустить: ./diagnose_pagekite.sh"
