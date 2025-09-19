#!/usr/bin/env python3
"""
HTTP версия webhook сервера для тестирования (без SSL)
"""

from flask import Flask, request, jsonify
import logging
from datetime import datetime
from database import Database
from prodamus import ProdаmusAPI
from config import PRODAMUS_SECRET_KEY, FLASK_HOST, FLASK_PORT

app = Flask(__name__)
logger = logging.getLogger(__name__)

# Инициализация компонентов
db = Database()
prodamus = ProdаmusAPI()

@app.route('/webhook/prodamus', methods=['POST'])
@app.route('/sales/prodamus', methods=['POST'])  # Дополнительный маршрут для Prodamus
def prodamus_webhook():
    """Обработчик webhook от Продамус"""
    try:
        # Получаем данные от Продамус
        data = request.get_json()
        
        if not data:
            logger.error("Пустые данные от webhook")
            return jsonify({'status': 'error', 'message': 'Empty data'}), 400
        
        # Получаем подпись из заголовков
        signature = request.headers.get('X-Signature')
        if not signature:
            signature = request.headers.get('Sign')  # Альтернативный заголовок
        
        logger.info(f"Получен webhook от Prodamus: {data}")
        logger.info(f"Подпись: {signature}")
        
        # Проверяем подпись
        if signature and not prodamus.verify_webhook(data, signature):
            logger.error("Неверная подпись webhook")
            return jsonify({'status': 'error', 'message': 'Invalid signature'}), 400
        
        # Обрабатываем платеж
        order_id = data.get('order_id')
        payment_status = data.get('payment_status')
        amount = float(data.get('sum', 0)) * 100  # Конвертируем в копейки
        
        logger.info(f"Обработка платежа: order_id={order_id}, status={payment_status}, amount={amount}")
        
        if payment_status == 'success':
            # Успешный платеж
            handle_successful_payment(order_id, int(amount), data)
            return jsonify({'status': 'success', 'message': 'Payment processed'})
        else:
            # Неуспешный платеж
            logger.info(f"Платеж не успешен: {payment_status}")
            return jsonify({'status': 'info', 'message': 'Payment not successful'})
            
    except Exception as e:
        logger.error(f"Ошибка обработки webhook: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

def handle_successful_payment(order_id: str, amount: int, webhook_data: dict):
    """Обработка успешного платежа"""
    try:
        # Извлекаем user_id из order_id (формат: women_club_{user_id}_{timestamp})
        if order_id.startswith('women_club_'):
            user_id_str = order_id.split('_')[2]  # Получаем user_id
            user_id = int(user_id_str)
        else:
            # Если формат не стандартный, пытаемся найти в данных
            user_id = webhook_data.get('customer_extra', {}).get('user_id')
            if not user_id:
                logger.error(f"Не удалось извлечь user_id из order_id: {order_id}")
                return
        
        username = webhook_data.get('customer_email', '').split('@')[0] if webhook_data.get('customer_email') else ''
        
        logger.info(f"Обработка успешного платежа: user_id={user_id}, order_id={order_id}, amount={amount}")

        # Обновляем статус платежа в базе данных
        db.add_payment(user_id, order_id, amount, 'success')

        # Создаем подписку
        db.create_subscription(user_id, order_id, amount)

        # Получаем информацию о пользователе
        user = db.get_user(user_id)
        subscription = db.get_active_subscription(user_id)

        logger.info(f"Подписка активирована для пользователя {user_id}")

        # Активируем подписку через бота
        try:
            import asyncio
            from bot import WomenClubBot

            bot = WomenClubBot()

            # Запускаем активацию подписки в новом event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            try:
                # Активируем подписку (добавляем в канал, отправляем уведомления)
                loop.run_until_complete(bot.activate_subscription(user_id, order_id, amount))
                logger.info(f"✅ Подписка активирована для пользователя {user_id}")
            finally:
                loop.close()

        except Exception as e:
            logger.error(f"Ошибка активации подписки: {e}")

    except Exception as e:
        logger.error(f"Ошибка обработки успешного платежа: {e}")

@app.route('/health', methods=['GET'])
def health_check():
    """Проверка здоровья сервера"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'service': 'webhook-server'
    })

@app.route('/test', methods=['GET', 'POST'])
def test_endpoint():
    """Тестовый endpoint"""
    if request.method == 'GET':
        return jsonify({
            'message': 'Webhook server is running',
            'timestamp': datetime.now().isoformat(),
            'method': 'GET'
        })
    else:
        data = request.get_json() or {}
        return jsonify({
            'message': 'Webhook server received data',
            'timestamp': datetime.now().isoformat(),
            'method': 'POST',
            'data': data
        })

if __name__ == '__main__':
    print("🚀 Запуск HTTP webhook сервера (без SSL)")
    print(f"🌐 URL: http://{FLASK_HOST}:{FLASK_PORT}")
    print(f"📡 Webhook: http://{FLASK_HOST}:{FLASK_PORT}/webhook/prodamus")
    print(f"📡 Sales: http://{FLASK_HOST}:{FLASK_PORT}/sales/prodamus")
    print(f"❤️ Health: http://{FLASK_HOST}:{FLASK_PORT}/health")
    print(f"🧪 Test: http://{FLASK_HOST}:{FLASK_PORT}/test")
    print()
    print("⚠️ ВАЖНО: Это HTTP сервер для тестирования!")
    print("   Для продакшена настройте HTTPS с SSL сертификатом")
    print()
    
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=True)
