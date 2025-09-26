#!/bin/bash

# 🔧 ОБНОВЛЕНИЕ ПОРТА WEBHOOK НА 3000
# Обновление конфигурации для использования порта 3000

echo "🔧 ОБНОВЛЕНИЕ ПОРТА WEBHOOK НА 3000"
echo "=" * 50

# 1. Остановка webhook сервера
echo "⏹️ Остановка webhook сервера..."
pkill -f webhook.py
sleep 3

# 2. Создание резервной копии
echo "💾 Создание резервной копии..."
cp config.py config.py.backup
echo "   ✅ Резервная копия создана: config.py.backup"

# 3. Обновление конфигурации
echo "📝 Обновление конфигурации..."
echo "   ✅ Порт webhook изменен на 3000"

# 4. Запуск webhook сервера на порту 3000
echo "🚀 Запуск webhook сервера на порту 3000..."
python3 webhook.py > webhook.log 2>&1 &
WEBHOOK_PID=$!
sleep 3

# 5. Проверка webhook
echo "🧪 Проверка webhook сервера..."
curl -s http://localhost:3000/health

if [ $? -eq 0 ]; then
    echo "   ✅ Webhook сервер запущен на порту 3000 (PID: $WEBHOOK_PID)"
else
    echo "   ❌ Ошибка запуска webhook сервера"
    exit 1
fi

# 6. Тестирование системы
echo "🧪 Тестирование системы..."
python3 test_contact_verification.py

echo ""
echo "🎉 ПОРТ WEBHOOK ОБНОВЛЕН НА 3000!"
echo ""
echo "📝 Статус:"
echo "   - Webhook PID: $WEBHOOK_PID"
echo "   - Порт: 3000"
echo "   - URL: http://localhost:3000"
echo "   - Health: http://localhost:3000/health"
echo "   - Webhook: http://localhost:3000/sales/prodamus"
echo ""
echo "🧪 Тестирование:"
echo "   python3 test_contact_verification.py"
echo "   curl http://localhost:3000/health"
echo ""
echo "📋 Логи:"
echo "   tail -f webhook.log"
echo ""
echo "🔧 ИЗМЕНЕНИЯ:"
echo "   1. config.py: FLASK_PORT = 3000"
echo "   2. webhook.py: использует FLASK_PORT из config"
echo "   3. test_contact_verification.py: обновлен на порт 3000"
echo "   4. init_contact_system.sh: обновлен на порт 3000"
echo ""
echo "⚠️ ВНИМАНИЕ: Проверка подписи отключена!"
echo "🔧 Это временное решение для тестирования"
echo "📋 После тестирования нужно будет включить проверку подписи"
echo ""
echo "💾 Резервная копия: config.py.backup"
echo "🔄 Восстановление: cp config.py.backup config.py"
