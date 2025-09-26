#!/bin/bash

# 🛑 ОСТАНОВКА СИСТЕМЫ
# Остановка всех компонентов системы

echo "🛑 ОСТАНОВКА СИСТЕМЫ ЖЕНСКОГО КЛУБА"
echo "=" * 50

# 1. Остановка webhook сервера
echo "⏹️ Остановка webhook сервера..."
pkill -f webhook.py
sleep 2

# 2. Остановка бота
echo "⏹️ Остановка Telegram бота..."
pkill -f main_with_pagekite.py
pkill -f bot.py
sleep 2

# 3. Остановка PageKite
echo "⏹️ Остановка PageKite..."
pkill -f pagekite.py
sleep 2

# 4. Проверка остановки
echo "🔍 Проверка остановки процессов..."
WEBHOOK_RUNNING=$(pgrep -f webhook.py)
BOT_RUNNING=$(pgrep -f "main_with_pagekite.py|bot.py")
PAGEKITE_RUNNING=$(pgrep -f pagekite.py)

if [ -z "$WEBHOOK_RUNNING" ] && [ -z "$BOT_RUNNING" ] && [ -z "$PAGEKITE_RUNNING" ]; then
    echo "✅ Все процессы остановлены"
else
    echo "⚠️ Некоторые процессы все еще работают:"
    [ -n "$WEBHOOK_RUNNING" ] && echo "   - Webhook: $WEBHOOK_RUNNING"
    [ -n "$BOT_RUNNING" ] && echo "   - Bot: $BOT_RUNNING"
    [ -n "$PAGEKITE_RUNNING" ] && echo "   - PageKite: $PAGEKITE_RUNNING"
    
    echo "🔧 Принудительная остановка..."
    pkill -9 -f webhook.py
    pkill -9 -f "main_with_pagekite.py|bot.py"
    pkill -9 -f pagekite.py
fi

echo ""
echo "🛑 СИСТЕМА ОСТАНОВЛЕНА!"
echo ""
echo "📋 Статус:"
echo "   - Webhook: остановлен"
echo "   - Bot: остановлен"
echo "   - PageKite: остановлен"
echo ""
echo "🚀 Запуск:"
echo "   ./start_system.sh"
