#!/bin/bash

# 🔍 ПРОВЕРКА СТАТУСА БОТА
# Проверка статуса бота, webhook сервера и PageKite

echo "🔍 ПРОВЕРКА СТАТУСА БОТА"
echo "=" * 50

# 1. Проверка процессов
echo "📋 Проверка процессов:"
echo "   - Webhook процессы:"
ps aux | grep webhook | grep -v grep
echo "   - PageKite процессы:"
ps aux | grep pagekite | grep -v grep
echo "   - Bot процессы:"
ps aux | grep main | grep -v grep
echo ""

# 2. Проверка портов
echo "📋 Проверка портов:"
echo "   - Порт 5000:"
netstat -tlnp | grep :5000
echo ""

# 3. Проверка локального webhook
echo "📋 Проверка локального webhook:"
curl -s http://localhost:5000/health
echo ""
echo ""

# 4. Проверка PageKite
echo "📋 Проверка PageKite:"
curl -s https://dashastar.pagekite.me/health
echo ""
echo ""

# 5. Проверка логов
echo "📋 Проверка логов:"
echo "   - Bot log (последние 5 строк):"
tail -5 bot.log 2>/dev/null || echo "   Лог не найден"
echo ""
echo "   - Webhook log (последние 5 строк):"
tail -5 webhook.log 2>/dev/null || echo "   Лог не найден"
echo ""
echo "   - PageKite log (последние 5 строк):"
tail -5 pagekite.log 2>/dev/null || echo "   Лог не найден"
echo ""

# 6. Проверка конфигурации
echo "📋 Проверка конфигурации:"
echo "   - PRODAMUS_WEBHOOK_URL: $(grep PRODAMUS_WEBHOOK_URL .env 2>/dev/null || echo 'Не найден')"
echo "   - WEBHOOK_URL: $(grep WEBHOOK_URL .env 2>/dev/null || echo 'Не найден')"
echo ""

# 7. Рекомендации
echo "📋 Рекомендации:"
if [ $(ps aux | grep webhook | grep -v grep | wc -l) -eq 0 ]; then
    echo "   ❌ Webhook не запущен - запустите: ./start_bot_with_webhook.sh"
fi

if [ $(ps aux | grep pagekite | grep -v grep | wc -l) -eq 0 ]; then
    echo "   ❌ PageKite не запущен - запустите: ./start_bot_with_webhook.sh"
fi

if [ $(ps aux | grep main | grep -v grep | wc -l) -eq 0 ]; then
    echo "   ❌ Bot не запущен - запустите: ./start_bot_with_webhook.sh"
fi

echo ""
echo "🎉 ПРОВЕРКА ЗАВЕРШЕНА!"
echo ""
echo "📝 Статус:"
echo "   - Webhook: $(ps aux | grep webhook | grep -v grep | wc -l) процессов"
echo "   - PageKite: $(ps aux | grep pagekite | grep -v grep | wc -l) процессов"
echo "   - Bot: $(ps aux | grep main | grep -v grep | wc -l) процессов"
echo ""
echo "🚀 Управление:"
echo "   - Запуск: ./start_bot_with_webhook.sh"
echo "   - Остановка: ./stop_bot_with_webhook.sh"
echo "   - Проверка: ./check_bot_status.sh"
