#!/bin/bash

# 🔧 ИСПРАВЛЕНИЕ PAGKITE И WEBHOOK
# Полное исправление проблем с PageKite и webhook сервером

echo "🔧 ИСПРАВЛЕНИЕ PAGKITE И WEBHOOK"
echo "=" * 50

# 1. Остановка всех процессов
echo "⏹️ Остановка всех процессов..."
pkill -f webhook.py
pkill -f webhook_http.py
pkill -f pagekite.py
pkill -f main.py
pkill -f python3
sleep 5

# 2. Проверка остановки
echo "🔍 Проверка остановки процессов..."
REMAINING_PROCESSES=$(ps aux | grep -E "(webhook|pagekite|main|python3)" | grep -v grep | wc -l)
if [ $REMAINING_PROCESSES -eq 0 ]; then
    echo "   ✅ Все процессы остановлены"
else
    echo "   ⚠️ Остались процессы:"
    ps aux | grep -E "(webhook|pagekite|main|python3)" | grep -v grep
    echo "   🔧 Принудительная остановка..."
    pkill -9 -f webhook.py
    pkill -9 -f pagekite.py
    pkill -9 -f main.py
    sleep 3
fi

# 3. Проверка портов
echo "🔍 Проверка портов..."
PORT_5000=$(netstat -tlnp | grep :5000 | wc -l)
if [ $PORT_5000 -gt 0 ]; then
    echo "   ⚠️ Порт 5000 занят:"
    netstat -tlnp | grep :5000
    echo "   🔧 Освобождение порта..."
    fuser -k 5000/tcp
    sleep 2
fi

# 4. Создание .env файла
echo "📝 Создание .env файла..."
cat > .env << 'EOF'
BOT_TOKEN=8455794146:AAFf9DEcTxLnJfG-HWWmzwpSjTRDzNE3px8
ADMIN_CHAT_ID=431292182,190545165
ADMIN_IDS=431292182,190545165
CHANNEL_ID=-1001234567890
CHANNEL_USERNAME=@your_channel_username
CHANNEL_INVITE_LINK=https://t.me/+gstVWYW2Kgo2OGYy
PRODAMUS_SHOP_ID=dashastar
PRODAMUS_SECRET_KEY=b2f9e8a399225271521dfe88a277a7371cb8c2cebfeaa6f0276ba81fcc303c93
PRODAMUS_DEMO_MODE=true
PRODAMUS_WEBHOOK_URL=https://dashastar.pagekite.me/sales/prodamus
WEBHOOK_URL=https://dashastar.pagekite.me/webhook/telegram
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
DEBUG=false
EOF

echo "✅ .env файл создан"

# 5. Проверка PageKite
echo "🔍 Проверка PageKite..."
if [ ! -f "pagekite.py" ]; then
    echo "   ⚠️ PageKite не найден, скачиваем..."
    wget -O pagekite.py https://pagekite.net/pk/pagekite.py
    chmod +x pagekite.py
    echo "   ✅ PageKite скачан"
else
    echo "   ✅ PageKite найден"
fi

# 6. Запуск webhook сервера
echo "🚀 Запуск webhook сервера..."
nohup python3 webhook.py > webhook.log 2>&1 &
WEBHOOK_PID=$!

# 7. Ожидание запуска webhook
echo "⏳ Ожидание запуска webhook сервера..."
sleep 5

# 8. Проверка webhook
echo "🧪 Проверка webhook сервера..."
WEBHOOK_STATUS=$(curl -s http://localhost:5000/health | grep -o '"status":"ok"' | wc -l)
if [ $WEBHOOK_STATUS -gt 0 ]; then
    echo "   ✅ Webhook сервер запущен (PID: $WEBHOOK_PID)"
else
    echo "   ❌ Ошибка запуска webhook сервера"
    echo "   📋 Логи webhook:"
    tail -20 webhook.log
    exit 1
fi

# 9. Запуск PageKite
echo "🌐 Запуск PageKite..."
nohup ./pagekite.py 5000 dashastar.pagekite.me > pagekite.log 2>&1 &
PAGKITE_PID=$!

# 10. Ожидание запуска PageKite
echo "⏳ Ожидание запуска PageKite..."
sleep 10

# 11. Проверка PageKite
echo "🧪 Проверка PageKite..."
PAGKITE_STATUS=$(curl -s https://dashastar.pagekite.me/health | grep -o '"status":"ok"' | wc -l)
if [ $PAGKITE_STATUS -gt 0 ]; then
    echo "   ✅ PageKite работает (PID: $PAGKITE_PID)"
else
    echo "   ❌ PageKite не работает"
    echo "   📋 Логи PageKite:"
    tail -20 pagekite.log
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

# 12. Финальная проверка
echo "🧪 Финальная проверка..."
echo "   - Webhook PID: $WEBHOOK_PID"
echo "   - PageKite PID: $PAGKITE_PID"
echo "   - Локальный health: $(curl -s http://localhost:5000/health)"
echo "   - Удаленный health: $(curl -s https://dashastar.pagekite.me/health)"

# 13. Проверка процессов
echo "🔍 Проверка процессов..."
ps aux | grep -E "(webhook|pagekite)" | grep -v grep

echo ""
echo "🎉 ИСПРАВЛЕНИЕ ЗАВЕРШЕНО!"
echo ""
echo "📝 Статус:"
echo "   - Webhook: PID $WEBHOOK_PID"
echo "   - PageKite: PID $PAGKITE_PID"
echo "   - Локальный URL: http://localhost:5000"
echo "   - Удаленный URL: https://dashastar.pagekite.me"
echo ""
echo "🧪 Тестирование:"
echo "   python3 check_webhook_status.py"
echo "   python3 test_post_webhook.py"
echo ""
echo "📋 Логи:"
echo "   tail -f webhook.log"
echo "   tail -f pagekite.log"
echo ""
echo "🔧 Управление:"
echo "   - Остановка: kill $WEBHOOK_PID $PAGKITE_PID"
echo "   - Перезапуск: ./fix_pagekite_webhook.sh"
