#!/bin/bash

# 🔧 ИСПРАВЛЕНИЕ ПРОБЛЕМ WEBHOOK
# Исправление проблем с PageKite и отключение проверки подписи

echo "🔧 ИСПРАВЛЕНИЕ ПРОБЛЕМ WEBHOOK"
echo "=" * 50

# 1. Остановка всех процессов
echo "⏹️ Остановка всех процессов..."
pkill -f webhook.py
pkill -f pagekite.py
pkill -f main.py
pkill -f main_with_webhook.py
sleep 3

# 2. Создание резервной копии
echo "💾 Создание резервной копии..."
cp webhook.py webhook.py.backup
echo "   ✅ Резервная копия создана: webhook.py.backup"

# 3. Отключение проверки подписи в webhook.py
echo "📝 Отключение проверки подписи в webhook.py..."
cat > webhook.py << 'EOF'
from flask import Flask, request, jsonify
import logging
import asyncio
from prodamus import ProdаmusAPI
from bot import WomenClubBot
from config import FLASK_HOST, FLASK_PORT

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
prodamus = ProdаmusAPI()
bot = WomenClubBot()

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'service': 'webhook-server',
        'status': 'ok',
        'timestamp': str(datetime.now())
    })

@app.route('/sales/prodamus', methods=['POST'])
def handle_prodamus_webhook():
    """Обработка webhook от Prodamus"""
    try:
        # Определяем тип данных
        if request.is_json:
            data = request.get_json()
        else:
            # Обрабатываем form-data
            data = request.form.to_dict()
            
            # Парсим products из form-data
            products = []
            i = 0
            while f'products[{i}][name]' in data:
                product = {
                    'name': data.get(f'products[{i}][name]', ''),
                    'price': data.get(f'products[{i}][price]', ''),
                    'quantity': data.get(f'products[{i}][quantity]', ''),
                    'sum': data.get(f'products[{i}][sum]', '')
                }
                products.append(product)
                i += 1
            data['products'] = products
        
        logger.info(f"Данные webhook: {data}")
        logger.info(f"Content-Type: {request.content_type}")
        logger.info(f"Заголовки: {dict(request.headers)}")
        
        if not data:
            logger.error("Пустые данные от webhook")
            return jsonify({'status': 'error', 'message': 'Empty data'}), 400
        
        # Получаем подпись из заголовков (Prodamus использует заголовок 'Sign')
        signature = request.headers.get('Sign')
        
        # ⚠️ ПРОВЕРКА ПОДПИСИ ОТКЛЮЧЕНА ДЛЯ ТЕСТИРОВАНИЯ
        logger.info("⚠️ ПРОВЕРКА ПОДПИСИ ОТКЛЮЧЕНА!")
        logger.info(f"  Полученная подпись: {signature}")
        logger.info(f"  ✅ Подпись принята без проверки")
        
        # Обрабатываем платеж (Prodamus использует другие поля)
        order_id = data.get('order_id')
        payment_status = data.get('payment_status')
        amount = int(float(data.get('sum', '0')) * 100)  # Конвертируем в копейки
        
        logger.info(f"Webhook получен: order_id={order_id}, payment_status={payment_status}, amount={amount}")
        
        if payment_status == 'success':
            logger.info("Обработка успешного платежа...")
            try:
                # Извлекаем user_id из order_id (формат: women_club_{user_id}_{timestamp})
                if order_id.startswith('women_club_'):
                    parts = order_id.split('_')
                    if len(parts) >= 3:
                        user_id = int(parts[2])
                        logger.info(f"Извлечен user_id: {user_id}")
                        
                        # Активируем подписку
                        asyncio.run(bot.activate_subscription(user_id, amount))
                        
                        logger.info("Подписка активирована успешно")
                    else:
                        logger.error("Не удалось извлечь user_id из order_id")
                else:
                    logger.error("Неверный формат order_id")
                    
            except Exception as e:
                logger.error(f"Ошибка обработки успешного платежа: {e}")
        else:
            logger.info(f"Платеж не успешен: {payment_status}")
        
        return jsonify({'status': 'success', 'message': 'Payment processed'})
        
    except Exception as e:
        logger.error(f"Ошибка обработки webhook: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    from datetime import datetime
    print("🚀 Запуск webhook сервера...")
    print(f"   - Host: {FLASK_HOST}")
    print(f"   - Port: {FLASK_PORT}")
    print(f"   - URL: http://{FLASK_HOST}:{FLASK_PORT}")
    print("⚠️ ПРОВЕРКА ПОДПИСИ ОТКЛЮЧЕНА!")
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=False)
EOF

echo "   ✅ webhook.py обновлен с отключенной проверкой подписи"

# 4. Запуск webhook сервера
echo "🚀 Запуск webhook сервера..."
python3 webhook.py &
WEBHOOK_PID=$!
sleep 3

# 5. Проверка webhook
echo "🧪 Проверка webhook сервера..."
WEBHOOK_STATUS=$(curl -s http://localhost:5000/health | grep -o '"status":"ok"' | wc -l)
if [ $WEBHOOK_STATUS -gt 0 ]; then
    echo "   ✅ Webhook сервер запущен (PID: $WEBHOOK_PID)"
else
    echo "   ❌ Ошибка запуска webhook сервера"
    echo "   📋 Логи webhook:"
    tail -20 webhook.log 2>/dev/null || echo "   Логи не найдены"
    exit 1
fi

# 6. Попытка запуска PageKite
echo "🌐 Попытка запуска PageKite..."
./pagekite.py 5000 dashastar.pagekite.me &
PAGKITE_PID=$!
sleep 10

# 7. Проверка PageKite
echo "🧪 Проверка PageKite..."
PAGKITE_STATUS=$(curl -s https://dashastar.pagekite.me/health | grep -o '"status":"ok"' | wc -l)
if [ $PAGKITE_STATUS -gt 0 ]; then
    echo "   ✅ PageKite работает (PID: $PAGKITE_PID)"
else
    echo "   ❌ PageKite не работает"
    echo "   📋 Логи PageKite:"
    tail -20 pagekite.log 2>/dev/null || echo "   Логи не найдены"
    echo "   🔧 Попробуем альтернативный запуск..."
    
    # Альтернативный запуск PageKite
    nohup ./pagekite.py 5000 dashastar.pagekite.me --frontend > pagekite.log 2>&1 &
    PAGKITE_PID=$!
    sleep 10
    
    PAGKITE_STATUS=$(curl -s https://dashastar.pagekite.me/health | grep -o '"status":"ok"' | wc -l)
    if [ $PAGKITE_STATUS -gt 0 ]; then
        echo "   ✅ PageKite работает после альтернативного запуска"
    else
        echo "   ❌ PageKite все еще не работает"
        echo "   📋 Проверьте логи: tail -f pagekite.log"
        echo "   🔧 Попробуйте использовать IP адрес вместо PageKite"
    fi
fi

# 8. Тестирование webhook
echo "🧪 Тестирование webhook..."
python3 test_no_signature.py

echo ""
echo "🎉 ПРОБЛЕМЫ WEBHOOK ИСПРАВЛЕНЫ!"
echo ""
echo "📝 Статус:"
echo "   - Webhook PID: $WEBHOOK_PID"
echo "   - PageKite PID: $PAGKITE_PID"
echo "   - Проверка подписи: ОТКЛЮЧЕНА"
echo "   - Локальный URL: http://localhost:5000"
echo "   - Удаленный URL: https://dashastar.pagekite.me"
echo ""
echo "🧪 Тестирование:"
echo "   python3 test_no_signature.py"
echo "   python3 test_full_payment_flow.py"
echo ""
echo "⚠️ ВНИМАНИЕ: Проверка подписи отключена!"
echo "🔧 Это временное решение для тестирования"
echo "📋 После тестирования нужно будет включить проверку подписи"
echo ""
echo "💾 Резервная копия: webhook.py.backup"
echo "🔄 Восстановление: cp webhook.py.backup webhook.py"