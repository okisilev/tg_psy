#!/bin/bash

# 🚀 БЫСТРЫЙ ЗАПУСК СИСТЕМЫ
# Запуск всех компонентов системы

echo "🚀 ЗАПУСК СИСТЕМЫ ЖЕНСКОГО КЛУБА"
echo "=" * 50

# 1. Проверка зависимостей
echo "🔍 Проверка зависимостей..."
python3 -c "import flask, requests, sqlite3" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Не все зависимости установлены"
    echo "📦 Установка зависимостей..."
    pip install -r requirements.txt
fi

# 2. Проверка конфигурации
echo "⚙️ Проверка конфигурации..."
python3 check_config.py

# 3. Инициализация базы данных
echo "🗄️ Инициализация базы данных..."
python3 init_database.py

# 4. Запуск webhook сервера
echo "🌐 Запуск webhook сервера..."
python3 webhook.py > webhook.log 2>&1 &
WEBHOOK_PID=$!
sleep 3

# 5. Проверка webhook
echo "🧪 Проверка webhook..."
curl -s http://localhost:3000/health > /dev/null
if [ $? -eq 0 ]; then
    echo "   ✅ Webhook запущен (PID: $WEBHOOK_PID)"
else
    echo "   ❌ Ошибка запуска webhook"
    exit 1
fi

# 6. Запуск бота
echo "🤖 Запуск Telegram бота..."
python3 main_with_pagekite.py &
BOT_PID=$!
sleep 3

echo ""
echo "🎉 СИСТЕМА ЗАПУЩЕНА!"
echo ""
echo "📝 Статус:"
echo "   - Webhook PID: $WEBHOOK_PID"
echo "   - Bot PID: $BOT_PID"
echo "   - Webhook URL: http://localhost:3000"
echo "   - Health: http://localhost:3000/health"
echo ""
echo "🧪 Тестирование:"
echo "   python3 run_tests.py"
echo "   python3 tests/test_contact_verification.py"
echo ""
echo "📋 Логи:"
echo "   tail -f webhook.log"
echo ""
echo "🛑 Остановка:"
echo "   pkill -f webhook.py"
echo "   pkill -f main_with_pagekite.py"
