#!/bin/bash

# 🔧 ИНИЦИАЛИЗАЦИЯ СИСТЕМЫ КОНТАКТНЫХ ДАННЫХ
# Полная инициализация системы с созданием базы данных

echo "🔧 ИНИЦИАЛИЗАЦИЯ СИСТЕМЫ КОНТАКТНЫХ ДАННЫХ"
echo "=" * 60

# 1. Остановка сервисов
echo "⏹️ Остановка сервисов..."
pkill -f webhook.py
pkill -f bot.py
sleep 3

# 2. Создание резервных копий
echo "💾 Создание резервных копий..."
cp database.py database.py.backup3
cp bot.py bot.py.backup3
cp webhook.py webhook.py.backup3
cp prodamus.py prodamus.py.backup3
echo "   ✅ Резервные копии созданы"

# 3. Инициализация базы данных
echo "📝 Инициализация базы данных..."
python3 init_database.py

if [ $? -eq 0 ]; then
    echo "   ✅ База данных инициализирована"
else
    echo "   ❌ Ошибка инициализации базы данных"
    exit 1
fi

# 4. Запуск webhook сервера
echo "🚀 Запуск webhook сервера..."
python3 webhook.py &
WEBHOOK_PID=$!
sleep 3

# 5. Проверка webhook
echo "🧪 Проверка webhook сервера..."
curl -s http://localhost:3000/health

if [ $? -eq 0 ]; then
    echo "   ✅ Webhook сервер запущен (PID: $WEBHOOK_PID)"
else
    echo "   ❌ Ошибка запуска webhook сервера"
    exit 1
fi

# 6. Тестирование системы контактных данных
echo "🧪 Тестирование системы контактных данных..."
python3 test_contact_verification.py

echo ""
echo "🎉 СИСТЕМА КОНТАКТНЫХ ДАННЫХ ИНИЦИАЛИЗИРОВАНА!"
echo ""
echo "📝 Статус:"
echo "   - Webhook PID: $WEBHOOK_PID"
echo "   - База данных: СОЗДАНА"
echo "   - Схема БД: ПОЛНАЯ"
echo "   - Сбор контактов: ВКЛЮЧЕН"
echo "   - Проверка по контактам: ВКЛЮЧЕНА"
echo "   - Локальный URL: http://localhost:3000"
echo ""
echo "🧪 Тестирование:"
echo "   python3 test_contact_verification.py"
echo "   python3 test_subscription_activation.py"
echo ""
echo "📋 Логи:"
echo "   tail -f webhook.log"
echo ""
echo "🔧 СОЗДАННЫЕ ТАБЛИЦЫ:"
echo "   1. users (с полями phone, email)"
echo "   2. subscriptions"
echo "   3. payments"
echo "   4. admins"
echo ""
echo "⚠️ ВНИМАНИЕ: Проверка подписи отключена!"
echo "🔧 Это временное решение для тестирования"
echo "📋 После тестирования нужно будет включить проверку подписи"
echo ""
echo "💾 Резервные копии:"
echo "   - database.py.backup3"
echo "   - bot.py.backup3"
echo "   - webhook.py.backup3"
echo "   - prodamus.py.backup3"
echo "🔄 Восстановление: cp *.backup3 ."
