from flask import Flask, request, jsonify
import logging
from datetime import datetime
from database import Database
from prodamus import ProdаmusAPI
from config import PRODAMUS_SECRET_KEY

app = Flask(__name__)
logger = logging.getLogger(__name__)

# Инициализация компонентов
db = Database()
prodamus = ProdаmusAPI()

@app.route('/webhook/prodamus', methods=['POST'])
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
            logger.error("Отсутствует подпись в webhook")
            return jsonify({'status': 'error', 'message': 'Missing signature'}), 400
        
        # Проверяем подпись
        if not prodamus.verify_webhook(data, signature):
            logger.error("Неверная подпись webhook")
            return jsonify({'status': 'error', 'message': 'Invalid signature'}), 400
        
        # Обрабатываем платеж
        order_id = data.get('order_id')
        status = data.get('status')
        amount = data.get('amount')
        
        logger.info(f"Webhook получен: order_id={order_id}, status={status}, amount={amount}")
        
        if status == 'success':
            # Платеж успешен
            handle_successful_payment(order_id, amount, data)
        elif status == 'failed':
            # Платеж не прошел
            handle_failed_payment(order_id, data)
        
        return jsonify({'status': 'success'})
        
    except Exception as e:
        logger.error(f"Ошибка обработки webhook: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

def handle_successful_payment(order_id: str, amount: int, webhook_data: dict):
    """Обработка успешного платежа"""
    try:
        # Извлекаем user_id из custom_fields
        custom_fields = webhook_data.get('custom_fields', {})
        user_id = int(custom_fields.get('user_id'))
        
        # Обновляем статус платежа в базе данных
        db.add_payment(user_id, order_id, amount, 'success')
        
        # Создаем подписку
        db.create_subscription(user_id, order_id, amount)
        
        # Получаем информацию о пользователе
        user = db.get_user(user_id)
        subscription = db.get_active_subscription(user_id)
        
        logger.info(f"Подписка активирована для пользователя {user_id}")
        
        # Здесь должна быть логика уведомления пользователя и администратора
        # В реальном проекте это делается через бота
        
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
