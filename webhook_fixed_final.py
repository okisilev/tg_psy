from flask import Flask, request, jsonify
import logging
import asyncio
from datetime import datetime, timedelta
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
            logger.info("Получен JSON webhook")
        else:
            data = request.form.to_dict()
            logger.info("Получен form-data webhook")
        
        # Логируем полученные данные
        logger.info(f"Webhook данные: {data}")
        
        # Извлекаем необходимые поля
        order_id = data.get('order_id')
        payment_status = data.get('payment_status')
        amount = int(float(data.get('sum', '0')) * 100)  # Конвертируем в копейки
        
        logger.info(f"Webhook получен: order_id={order_id}, payment_status={payment_status}, amount={amount}")
        
        if payment_status == 'success':
            logger.info("Обработка успешного платежа...")
            try:
                # Получаем контактные данные из webhook
                customer_phone = data.get('customer_phone', '')
                customer_email = data.get('customer_email', '')
                
                logger.info(f"Контактные данные из webhook: phone={customer_phone}, email={customer_email}")
                
                # Ищем пользователя по контактным данным
                user_id = None
                
                if customer_phone:
                    user_id = db.find_user_by_phone(customer_phone)
                    logger.info(f"Поиск по телефону {customer_phone}: user_id={user_id}")
                
                if not user_id and customer_email:
                    user_id = db.find_user_by_email(customer_email)
                    logger.info(f"Поиск по email {customer_email}: user_id={user_id}")
                
                # Если не нашли по контактам, пробуем извлечь из order_id
                if not user_id and order_id.startswith('women_club_'):
                    parts = order_id.split('_')
                    if len(parts) >= 3:
                        user_id = int(parts[2])
                        logger.info(f"Извлечен user_id из order_id: {user_id}")
                
                if user_id:
                    logger.info(f"Найден user_id: {user_id}")
                    
                    # Активируем подписку напрямую
                    try:
                        # Создаем подписку
                        start_date = datetime.now()
                        end_date = start_date + timedelta(days=30)
                        
                        db.add_subscription(
                            user_id=user_id,
                            payment_id=order_id,
                            amount=amount,
                            start_date=start_date,
                            end_date=end_date
                        )
                        
                        # Обновляем статус платежа
                        db.update_payment_status(order_id, 'completed')
                        
                        logger.info("Подписка активирована успешно")
                    except Exception as e:
                        logger.error(f"Ошибка активации подписки: {e}")
                else:
                    logger.error("Не удалось найти пользователя по контактным данным или order_id")
                    
            except Exception as e:
                logger.error(f"Ошибка обработки успешного платежа: {e}")
        elif payment_status == 'failed':
            logger.info(f"Платеж не прошел: {order_id}")
        
        return jsonify({'status': 'success'})
        
    except Exception as e:
        logger.error(f"Ошибка обработки webhook: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Проверка состояния сервера"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=True)
