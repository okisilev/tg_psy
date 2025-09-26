#!/bin/bash

# 🔧 ЗАМЕНА WEBHOOK НА ИСПРАВЛЕННУЮ ВЕРСИЮ
# Замена webhook.py на исправленную версию

echo "🔧 ЗАМЕНА WEBHOOK НА ИСПРАВЛЕННУЮ ВЕРСИЮ"
echo "=" * 60

# 1. Остановка webhook сервера
echo "⏹️ Остановка webhook сервера..."
pkill -f webhook_http.py
pkill -f webhook.py
sleep 2

# 2. Создание резервной копии
echo "💾 Создание резервной копии..."
cp webhook.py webhook.py.backup
echo "   ✅ Резервная копия создана: webhook.py.backup"

# 3. Замена на исправленную версию
echo "🔄 Замена на исправленную версию..."
cp webhook_fixed.py webhook.py
echo "   ✅ Webhook заменен на исправленную версию"

# 4. Обновление переменных окружения
echo "⚙️ Обновление переменных окружения..."
export FLASK_PORT="5000"
export PRODAMUS_WEBHOOK_URL="https://dashastar.pagekite.me/sales/prodamus"
export WEBHOOK_URL="https://dashastar.pagekite.me/webhook/telegram"

echo "✅ Переменные окружения обновлены"

# 5. Создание .env файла
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

# 6. Запуск исправленного webhook сервера
echo "🚀 Запуск исправленного webhook сервера..."
python3 webhook.py &

# 7. Ожидание запуска
echo "⏳ Ожидание запуска..."
sleep 3

# 8. Проверка работы
echo "🧪 Проверка работы..."
curl -s http://localhost:5000/health

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Исправленный webhook сервер запущен успешно!"
    echo ""
    echo "🔧 ИСПРАВЛЕНИЯ:"
    echo "   ✅ Webhook обрабатывает form-data"
    echo "   ✅ Обработка массивов в form-data (products)"
    echo "   ✅ Исправлена ошибка 'str' object has no attribute 'get'"
    echo "   ✅ Добавлено подробное логирование"
    echo "   ✅ Улучшена обработка ошибок"
    echo ""
    echo "🧪 Тест webhook:"
    echo "   python3 test_webhook_form_data.py"
    echo ""
    echo "📝 Настройки для Prodamus:"
    echo "   - Webhook URL: https://dashastar.pagekite.me/sales/prodamus"
    echo "   - Метод: POST"
    echo "   - Заголовки: Sign: {signature}"
    echo "   - Content-Type: application/x-www-form-urlencoded"
else
    echo "❌ Ошибка запуска webhook сервера"
    exit 1
fi

echo ""
echo "🎉 WEBHOOK ЗАМЕНЕН НА ИСПРАВЛЕННУЮ ВЕРСИЮ!"
echo "✅ Теперь webhook будет правильно обрабатывать все данные от Prodamus"
