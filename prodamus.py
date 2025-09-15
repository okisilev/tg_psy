import requests
import hashlib
import hmac
import json
import time
from typing import Dict, Optional
from config import (
    PRODAMUS_SHOP_ID, 
    PRODAMUS_SECRET_KEY, 
    PRODAMUS_API_URL,
    SUBSCRIPTION_PRICE
)

class ProdаmusAPI:
    def __init__(self):
        self.shop_id = PRODAMUS_SHOP_ID
        self.secret_key = PRODAMUS_SECRET_KEY
        self.api_url = PRODAMUS_API_URL
    
    def generate_signature(self, data: str) -> str:
        """Генерация подписи для запроса к Продамус"""
        return hmac.new(
            self.secret_key.encode('utf-8'),
            data.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
    
    def create_payment(self, user_id: int, username: str = None) -> Optional[Dict]:
        """Создание платежа в Продамус"""
        try:
            payment_data = {
                'shop_id': self.shop_id,
                'amount': SUBSCRIPTION_PRICE,
                'currency': 'RUB',
                'order_id': f'women_club_{user_id}_{int(time.time())}',
                'customer_phone': '',
                'customer_email': '',
                'description': 'Подписка на Женский клуб на 1 месяц',
                'success_url': 'https://t.me/your_bot_username',  # URL после успешной оплаты
                'fail_url': 'https://t.me/your_bot_username',     # URL после неуспешной оплаты
                'callback_url': 'https://yourdomain.com/webhook',  # Webhook для уведомлений
                'custom_fields': {
                    'user_id': user_id,
                    'username': username or ''
                }
            }
            
            # Создаем строку для подписи
            sign_string = f"{payment_data['shop_id']}{payment_data['amount']}{payment_data['order_id']}{payment_data['currency']}{self.secret_key}"
            payment_data['signature'] = self.generate_signature(sign_string)
            
            response = requests.post(self.api_url, json=payment_data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('status') == 'success':
                    return {
                        'payment_id': result.get('order_id'),
                        'payment_url': result.get('payment_url'),
                        'amount': payment_data['amount']
                    }
            
            return None
            
        except Exception as e:
            print(f"Ошибка создания платежа: {e}")
            return None
    
    def verify_webhook(self, data: Dict, signature: str) -> bool:
        """Проверка подписи webhook от Продамус"""
        try:
            # Создаем строку для проверки подписи
            sign_data = f"{data.get('shop_id')}{data.get('amount')}{data.get('order_id')}{data.get('currency')}{data.get('status')}{self.secret_key}"
            expected_signature = self.generate_signature(sign_data)
            
            return hmac.compare_digest(signature, expected_signature)
        except Exception as e:
            print(f"Ошибка проверки подписи: {e}")
            return False
    
    def get_payment_status(self, order_id: str) -> Optional[Dict]:
        """Получение статуса платежа"""
        try:
            url = f"https://secure.payform.ru/status"
            data = {
                'shop_id': self.shop_id,
                'order_id': order_id,
                'signature': self.generate_signature(f"{self.shop_id}{order_id}{self.secret_key}")
            }
            
            response = requests.post(url, json=data, timeout=30)
            
            if response.status_code == 200:
                return response.json()
            
            return None
            
        except Exception as e:
            print(f"Ошибка получения статуса платежа: {e}")
            return None
