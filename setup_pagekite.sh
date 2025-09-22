#!/bin/bash

# 🚀 НАСТРОЙКА PAGKITE ДЛЯ WEBHOOK
# Создание публичного URL для webhook через PageKite

echo "🚀 НАСТРОЙКА PAGKITE ДЛЯ WEBHOOK"
echo "=" * 50

# 1. Установка PageKite
echo "📦 Установка PageKite..."

# Скачиваем PageKite
wget https://pagekite.net/pk/pagekite.py
chmod +x pagekite.py

if [ $? -eq 0 ]; then
    echo "   ✅ PageKite скачан успешно"
else
    echo "   ❌ Ошибка скачивания PageKite"
    exit 1
fi

# 2. Остановка webhook сервера
echo "⏹️ Остановка webhook сервера..."
pkill -f webhook_http.py
sleep 2

# 3. Обновление переменных окружения
echo "⚙️ Обновление переменных окружения..."
export FLASK_PORT="5000"
export PRODAMUS_WEBHOOK_URL="https://dashastar.pagekite.me/sales/prodamus"
export WEBHOOK_URL="https://dashastar.pagekite.me/webhook/telegram"

echo "✅ Переменные окружения обновлены"

# 4. Создание .env файла с PageKite URL
echo "📝 Создание .env файла с PageKite URL..."
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

echo "✅ .env файл создан с PageKite URL"

# 5. Запуск webhook сервера
echo "🚀 Запуск webhook сервера..."
python3 webhook_http.py &

# 6. Ожидание запуска
echo "⏳ Ожидание запуска webhook сервера..."
sleep 3

# 7. Проверка работы webhook
echo "🧪 Проверка работы webhook..."
curl -s http://localhost:5000/health

if [ $? -eq 0 ]; then
    echo "   ✅ Webhook сервер запущен"
else
    echo "   ❌ Ошибка запуска webhook сервера"
    exit 1
fi

# 8. Запуск PageKite
echo "🌐 Запуск PageKite..."
echo "   - Домен: dashastar.pagekite.me"
echo "   - Порт: 5000"
echo "   - Команда: ./pagekite.py 5000 dashastar.pagekite.me"

# Запускаем PageKite в фоне
./pagekite.py 5000 dashastar.pagekite.me &

# 9. Ожидание запуска PageKite
echo "⏳ Ожидание запуска PageKite..."
sleep 5

# 10. Проверка PageKite
echo "🧪 Проверка PageKite..."
curl -s https://dashastar.pagekite.me/health

if [ $? -eq 0 ]; then
    echo "   ✅ PageKite работает"
    echo ""
    echo "🎉 PAGKITE НАСТРОЕН УСПЕШНО!"
    echo ""
    echo "📝 Настройки для Prodamus:"
    echo "   - Webhook URL: https://dashastar.pagekite.me/sales/prodamus"
    echo "   - Метод: POST"
    echo "   - Заголовки: Sign: {signature}"
    echo ""
    echo "📝 Настройки для Telegram:"
    echo "   - Webhook URL: https://dashastar.pagekite.me/webhook/telegram"
    echo "   - Метод: POST"
    echo ""
    echo "🧪 Тест webhook через PageKite:"
    echo "   curl -X POST https://dashastar.pagekite.me/sales/prodamus \\"
    echo "     -H 'Content-Type: application/json' \\"
    echo "     -H 'Sign: 30ba444dc24a268bdb78669632c6e0777652c0e63217b6cbc9adcb5fb2a0adaa' \\"
    echo "     -d '{\"order_id\":\"women_club_431292182_test\",\"sum\":\"50.00\",\"currency\":\"rub\",\"payment_status\":\"success\"}'"
else
    echo "   ❌ PageKite не работает"
    echo "   🔧 Проверьте настройки PageKite"
fi

echo ""
echo "✅ PAGKITE НАСТРОЕН!"
echo "🌐 Webhook доступен по адресу: https://dashastar.pagekite.me"
