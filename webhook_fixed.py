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
    from datetime import datetime
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
        elif payment_status == 'failed':
            logger.info(f"Платеж не прошел: {order_id}")
        
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