#!/bin/bash

# 🚀 ЗАПУСК ПОЛНОЙ СИСТЕМЫ
# Запуск бота с webhook сервером и PageKite

echo "🚀 ЗАПУСК ПОЛНОЙ СИСТЕМЫ"
echo "=" * 50

# 1. Остановка старых процессов
echo "⏹️ Остановка старых процессов..."
pkill -f webhook.py
pkill -f pagekite.py
pkill -f main.py
pkill -f main_with_pagekite.py
sleep 3

# 2. Установка PageKite
echo "📥 Установка PageKite..."
./install_pagekite.sh

# 3. Запуск полной системы
echo "🚀 Запуск полной системы..."
python3 main_with_pagekite.py &
SYSTEM_PID=$!
sleep 5

# 4. Проверка системы
echo "🧪 Проверка системы..."
echo "   - Локальный health: $(curl -s http://localhost:5000/health)"
echo "   - Удаленный health: $(curl -s https://dashastar.pagekite.me/health)"

# 5. Проверка процессов
echo "🔍 Проверка процессов..."
ps aux | grep -E "(webhook|pagekite|main)" | grep -v grep

echo ""
echo "🎉 ПОЛНАЯ СИСТЕМА ЗАПУЩЕНА!"
echo ""
echo "📝 Статус:"
echo "   - System PID: $SYSTEM_PID"
echo "   - Локальный URL: http://localhost:5000"
echo "   - Удаленный URL: https://dashastar.pagekite.me"
echo ""
echo "🧪 Тестирование:"
echo "   python3 test_payment_processing.py"
echo "   python3 test_no_signature.py"
echo ""
echo "📋 Логи:"
echo "   tail -f bot.log"
echo "   tail -f webhook.log"
echo ""
echo "🛑 Остановка:"
echo "   pkill -f main_with_pagekite.py"
echo "   ./stop_pagekite.sh"
