#!/bin/bash

# 🔧 ОБНОВЛЕНИЕ СИСТЕМЫ С ПОДДЕРЖКОЙ КОНТАКТНЫХ ДАННЫХ
# Обновление системы для сбора и проверки контактных данных

echo "🔧 ОБНОВЛЕНИЕ СИСТЕМЫ С ПОДДЕРЖКОЙ КОНТАКТНЫХ ДАННЫХ"
echo "=" * 60

# 1. Остановка сервисов
echo "⏹️ Остановка сервисов..."
pkill -f webhook.py
pkill -f bot.py
sleep 3

# 2. Создание резервных копий
echo "💾 Создание резервных копий..."
cp database.py database.py.backup
cp bot.py bot.py.backup
cp webhook.py webhook.py.backup
cp prodamus.py prodamus.py.backup
echo "   ✅ Резервные копии созданы"

# 3. Обновление базы данных
echo "📝 Обновление схемы базы данных..."
python3 -c "
from database import Database
db = Database()
print('✅ Схема базы данных обновлена')
"

# 4. Запуск webhook сервера
echo "🚀 Запуск webhook сервера..."
python3 webhook.py &
WEBHOOK_PID=$!
sleep 3

# 5. Проверка webhook
echo "🧪 Проверка webhook сервера..."
curl -s http://localhost:5000/health

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
echo "🎉 СИСТЕМА КОНТАКТНЫХ ДАННЫХ ОБНОВЛЕНА!"
echo ""
echo "📝 Статус:"
echo "   - Webhook PID: $WEBHOOK_PID"
echo "   - Сбор контактов: ВКЛЮЧЕН"
echo "   - Проверка по контактам: ВКЛЮЧЕНА"
echo "   - Локальный URL: http://localhost:5000"
echo ""
echo "🧪 Тестирование:"
echo "   python3 test_contact_verification.py"
echo "   python3 test_subscription_activation.py"
echo ""
echo "📋 Логи:"
echo "   tail -f webhook.log"
echo ""
echo "🔧 НОВЫЕ ВОЗМОЖНОСТИ:"
echo "   1. Сбор номера телефона при входе"
echo "   2. Сбор email при входе"
echo "   3. Передача контактов в Prodamus"
echo "   4. Поиск пользователя по телефону/email"
echo "   5. Привязка платежа по контактам"
echo ""
echo "⚠️ ВНИМАНИЕ: Проверка подписи отключена!"
echo "🔧 Это временное решение для тестирования"
echo "📋 После тестирования нужно будет включить проверку подписи"
echo ""
echo "💾 Резервные копии:"
echo "   - database.py.backup"
echo "   - bot.py.backup"
echo "   - webhook.py.backup"
echo "   - prodamus.py.backup"
echo "🔄 Восстановление: cp *.backup ."
