#!/bin/bash

# 🚀 БЫСТРЫЙ ЗАПУСК С PAGKITE
# Простой запуск бота с webhook и PageKite

echo "🚀 БЫСТРЫЙ ЗАПУСК С PAGKITE"
echo "=" * 50

# 1. Остановка старых процессов
echo "⏹️ Остановка старых процессов..."
pkill -f webhook.py
pkill -f pagekite.py
pkill -f main.py
pkill -f main_with_pagekite.py
sleep 2

# 2. Проверка PageKite
echo "🔍 Проверка PageKite..."
if [ ! -f "pagekite.py" ]; then
    echo "   📥 Скачивание pagekite.py..."
    wget -O pagekite.py https://pagekite.net/pk/pagekite.py
    chmod +x pagekite.py
    echo "   ✅ pagekite.py установлен"
else
    echo "   ✅ pagekite.py уже установлен"
fi

# 3. Запуск системы
echo "🚀 Запуск системы..."
python3 main_with_pagekite.py &
SYSTEM_PID=$!

# 4. Ожидание запуска
echo "⏳ Ожидание запуска..."
sleep 15

# 5. Проверка статуса
echo "🧪 Проверка статуса..."
echo "   - Локальный health: $(curl -s http://localhost:5000/health)"
echo "   - Удаленный health: $(curl -s https://dashastar.pagekite.me/health)"

echo ""
echo "🎉 СИСТЕМА ЗАПУЩЕНА!"
echo ""
echo "📝 Статус:"
echo "   - System PID: $SYSTEM_PID"
echo "   - Локальный URL: http://localhost:5000"
echo "   - Удаленный URL: https://dashastar.pagekite.me"
echo ""
echo "🧪 Тестирование:"
echo "   python3 test_payment_processing.py"
echo ""
echo "🛑 Остановка:"
echo "   pkill -f main_with_pagekite.py"
