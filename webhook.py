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
        # Получаем данные от Продамус (form-data или JSON)
        if request.is_json:
            data = request.get_json()
            logger.info("Получены JSON данные от webhook")
        else:
            # Обрабатываем form-data
            data = request.form.to_dict()
            logger.info("Получены form-data от webhook")
            
            # Обрабатываем массивы в form-data (например, products)
            if 'products[0][name]' in data:
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
        
        if not signature:
            logger.error("Отсутствует подпись в webhook")
            return jsonify({'status': 'error', 'message': 'Missing signature'}), 400
        
        # Проверяем подпись
        if not prodamus.verify_webhook(data, signature):
            logger.error("Неверная подпись webhook")
            return jsonify({'status': 'error', 'message': 'Invalid signature'}), 400
        
        # Обрабатываем платеж (Prodamus использует другие поля)
        order_id = data.get('order_id')
        payment_status = data.get('payment_status')
        amount = int(float(data.get('sum', '0')) * 100)  # Конвертируем в копейки
        
        logger.info(f"Webhook получен: order_id={order_id}, payment_status={payment_status}, amount={amount}")
        
        if payment_status == 'success':
            # Платеж успешен
            handle_successful_payment(order_id, amount, data)
        elif payment_status == 'failed':
            # Платеж не прошел
            handle_failed_payment(order_id, data)
        
        return jsonify({'status': 'success'})
        
    except Exception as e:
        logger.error(f"Ошибка обработки webhook: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

def handle_successful_payment(order_id: str, amount: int, webhook_data: dict):
    """Обработка успешного платежа"""
    try:
        # Извлекаем user_id из order_id (формат: women_club_{user_id}_{timestamp})
        if order_id.startswith('women_club_'):
            user_id = int(order_id.split('_')[2])
        else:
            logger.error(f"Неверный формат order_id: {order_id}")
            return
        
        # Получаем email для логирования
        customer_email = webhook_data.get('customer_email', '')
        
        logger.info(f"Обработка успешного платежа: user_id={user_id}, order_id={order_id}, amount={amount}, email={customer_email}")
        
        # Обновляем статус платежа в базе данных
        db.add_payment(user_id, order_id, amount, 'success')
        
        # Создаем подписку
        db.create_subscription(user_id, order_id, amount)
        
        # Получаем информацию о пользователе
        user = db.get_user(user_id)
        subscription = db.get_active_subscription(user_id)
        
        username = user.get('username', 'Unknown') if user else 'Unknown'
        logger.info(f"Подписка активирована для пользователя {user_id} (username: {username})")
        
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

def handle_failed_payment(order_id: str, webhook_data: dict):
    """Обработка неудачного платежа"""
    try:
        # Извлекаем user_id из custom_fields
        custom_fields = webhook_data.get('custom_fields', {})
        user_id = int(custom_fields.get('user_id'))
        
        # Обновляем статус платежа в базе данных
        amount = webhook_data.get('amount', 0)
        db.add_payment(user_id, order_id, amount, 'failed')
        
        logger.info(f"Платеж не прошел для пользователя {user_id}")
        
        # Здесь должна быть логика уведомления пользователя об ошибке платежа
        
    except Exception as e:
        logger.error(f"Ошибка обработки неудачного платежа: {e}")

@app.route('/health', methods=['GET'])
def health_check():
    """Проверка здоровья сервиса"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
