#!/bin/bash

# ⏹️ ОСТАНОВКА PAGKITE И WEBHOOK СЕРВЕРА
# Остановка всех сервисов

echo "⏹️ ОСТАНОВКА PAGKITE И WEBHOOK СЕРВЕРА"
echo "=" * 50

# 1. Остановка webhook сервера
echo "⏹️ Остановка webhook сервера..."
pkill -f webhook_http.py

if [ $? -eq 0 ]; then
    echo "   ✅ Webhook сервер остановлен"
else
    echo "   ⚠️ Webhook сервер не был запущен"
fi

# 2. Остановка PageKite
echo "⏹️ Остановка PageKite..."
pkill -f pagekite.py

if [ $? -eq 0 ]; then
    echo "   ✅ PageKite остановлен"
else
    echo "   ⚠️ PageKite не был запущен"
fi

# 3. Ожидание завершения процессов
echo "⏳ Ожидание завершения процессов..."
sleep 2

# 4. Проверка процессов
echo "🔍 Проверка процессов..."
WEBHOOK_PROCESSES=$(ps aux | grep webhook_http.py | grep -v grep | wc -l)
PAGKITE_PROCESSES=$(ps aux | grep pagekite.py | grep -v grep | wc -l)

if [ $WEBHOOK_PROCESSES -eq 0 ]; then
    echo "   ✅ Webhook сервер остановлен"
else
    echo "   ⚠️ Webhook сервер все еще работает"
fi

if [ $PAGKITE_PROCESSES -eq 0 ]; then
    echo "   ✅ PageKite остановлен"
else
    echo "   ⚠️ PageKite все еще работает"
fi

# 5. Проверка портов
echo "🔍 Проверка портов..."
PORT_5000=$(netstat -tlnp | grep :5000 | wc -l)

if [ $PORT_5000 -eq 0 ]; then
    echo "   ✅ Порт 5000 свободен"
else
    echo "   ⚠️ Порт 5000 все еще занят"
fi

echo ""
echo "✅ СЕРВИСЫ ОСТАНОВЛЕНЫ!"
echo ""
echo "🔧 Для повторного запуска используйте:"
echo "   ./start_pagekite_webhook.sh"
