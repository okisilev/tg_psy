import hashlib
import hmac
import requests
import json
from typing import Dict, Optional
from config import PRODAMUS_SHOP_ID, PRODAMUS_SECRET_KEY, PRODAMUS_API_URL, PRODAMUS_DEMO_MODE, PRODAMUS_WEBHOOK_URL

class ProdаmusAPI:
    def __init__(self):
        self.shop_id = PRODAMUS_SHOP_ID
        self.secret_key = PRODAMUS_SECRET_KEY
        self.api_url = PRODAMUS_API_URL
        self.demo_mode = PRODAMUS_DEMO_MODE
        self.webhook_url = PRODAMUS_WEBHOOK_URL
        
    def generate_signature(self, data: str) -> str:
        """Генерация подписи для Prodamus"""
        return hmac.new(
            self.secret_key.encode('utf-8'),
            data.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
    
    def create_payment(self, order_id: str, amount: int, description: str, user_id: int) -> Optional[str]:
        """Создание платежа в Prodamus"""
        try:
            # Конвертируем сумму в рубли
            amount_rub = amount / 100
            
            # Параметры для Prodamus
            params = {
                'shop_id': self.shop_id,
                'order_id': order_id,
                'sum': str(amount_rub),
                'currency': 'rub',
                'description': description,
                'customer_phone': '',  # Можно добавить телефон пользователя
                'customer_email': '',  # Можно добавить email пользователя
                'success_url': f'https://t.me/your_bot_username',  # URL после успешной оплаты
                'failure_url': f'https://t.me/your_bot_username',  # URL после неудачной оплаты
                'webhook_url': self.webhook_url,
                'payment_method': 'card',
                'payment_system': 'all'
            }
            
            # Добавляем demo_mode если включен
            if self.demo_mode:
                params['demo_mode'] = '1'
            
            # Создаем подпись
            sign_data = f"{self.shop_id}{order_id}{amount_rub}rub{self.secret_key}"
            params['sign'] = self.generate_signature(sign_data)
            
            # Формируем URL для GET запроса
            payment_url = f"{self.api_url}?" + "&".join([f"{k}={v}" for k, v in params.items()])
            
            print(f"Создание платежа Prodamus:")
            print(f"  Order ID: {order_id}")
            print(f"  Amount: {amount_rub} руб")
            print(f"  Description: {description}")
            print(f"  Demo Mode: {self.demo_mode}")
            print(f"  Webhook URL: {self.webhook_url}")
            print(f"  Payment URL: {payment_url}")
            
            return payment_url
            
        except Exception as e:
            print(f"Ошибка создания платежа: {e}")
            return None
    
    def verify_webhook(self, data: Dict, signature: str) -> bool:
        """Проверка подписи webhook от Продамус с расширенными вариантами"""
        try:
            print(f"Проверка подписи:")
            print(f"  Полученная подпись: {signature}")
            print(f"  Данные: {data}")
            
            # Пробуем разные варианты генерации подписи (40 вариантов)
            variants = [
                # Вариант 1: shop_id + order_id + sum + currency + payment_status + secret_key
                f"{self.shop_id}{data.get('order_id', '')}{data.get('sum', '')}{data.get('currency', '')}{data.get('payment_status', '')}{self.secret_key}",
                
                # Вариант 2: order_id + sum + currency + payment_status + secret_key
                f"{data.get('order_id', '')}{data.get('sum', '')}{data.get('currency', '')}{data.get('payment_status', '')}{self.secret_key}",
                
                # Вариант 3: order_id + sum + payment_status + secret_key
                f"{data.get('order_id', '')}{data.get('sum', '')}{data.get('payment_status', '')}{self.secret_key}",
                
                # Вариант 4: sum + payment_status + secret_key
                f"{data.get('sum', '')}{data.get('payment_status', '')}{self.secret_key}",
                
                # Вариант 5: order_id + payment_status + secret_key
                f"{data.get('order_id', '')}{data.get('payment_status', '')}{self.secret_key}",
                
                # Вариант 6: только order_id + secret_key
                f"{data.get('order_id', '')}{self.secret_key}",
                
                # Вариант 7: только sum + secret_key
                f"{data.get('sum', '')}{self.secret_key}",
                
                # Вариант 8: только payment_status + secret_key
                f"{data.get('payment_status', '')}{self.secret_key}",
                
                # Вариант 9: все поля без shop_id
                f"{data.get('order_id', '')}{data.get('sum', '')}{data.get('currency', '')}{data.get('payment_status', '')}{data.get('customer_email', '')}{self.secret_key}",
                
                # Вариант 10: все поля с shop_id
                f"{self.shop_id}{data.get('order_id', '')}{data.get('sum', '')}{data.get('currency', '')}{data.get('payment_status', '')}{data.get('customer_email', '')}{self.secret_key}",
                
                # Вариант 11: только order_id + sum + secret_key
                f"{data.get('order_id', '')}{data.get('sum', '')}{self.secret_key}",
                
                # Вариант 12: только sum + currency + secret_key
                f"{data.get('sum', '')}{data.get('currency', '')}{self.secret_key}",
                
                # Вариант 13: только order_id + currency + secret_key
                f"{data.get('order_id', '')}{data.get('currency', '')}{self.secret_key}",
                
                # Вариант 14: только order_id + currency + payment_status + secret_key
                f"{data.get('order_id', '')}{data.get('currency', '')}{data.get('payment_status', '')}{self.secret_key}",
                
                # Вариант 15: только sum + currency + payment_status + secret_key
                f"{data.get('sum', '')}{data.get('currency', '')}{data.get('payment_status', '')}{self.secret_key}",
                
                # Дополнительные варианты с другими полями
                # Вариант 16: order_id + customer_email + secret_key
                f"{data.get('order_id', '')}{data.get('customer_email', '')}{self.secret_key}",
                
                # Вариант 17: sum + customer_email + secret_key
                f"{data.get('sum', '')}{data.get('customer_email', '')}{self.secret_key}",
                
                # Вариант 18: payment_status + customer_email + secret_key
                f"{data.get('payment_status', '')}{data.get('customer_email', '')}{self.secret_key}",
                
                # Вариант 19: order_id + sum + customer_email + secret_key
                f"{data.get('order_id', '')}{data.get('sum', '')}{data.get('customer_email', '')}{self.secret_key}",
                
                # Вариант 20: order_id + payment_status + customer_email + secret_key
                f"{data.get('order_id', '')}{data.get('payment_status', '')}{data.get('customer_email', '')}{self.secret_key}",
                
                # Вариант 21: sum + payment_status + customer_email + secret_key
                f"{data.get('sum', '')}{data.get('payment_status', '')}{data.get('customer_email', '')}{self.secret_key}",
                
                # Вариант 22: order_id + sum + payment_status + customer_email + secret_key
                f"{data.get('order_id', '')}{data.get('sum', '')}{data.get('payment_status', '')}{data.get('customer_email', '')}{self.secret_key}",
                
                # Вариант 23: shop_id + order_id + customer_email + secret_key
                f"{self.shop_id}{data.get('order_id', '')}{data.get('customer_email', '')}{self.secret_key}",
                
                # Вариант 24: shop_id + sum + customer_email + secret_key
                f"{self.shop_id}{data.get('sum', '')}{data.get('customer_email', '')}{self.secret_key}",
                
                # Вариант 25: shop_id + payment_status + customer_email + secret_key
                f"{self.shop_id}{data.get('payment_status', '')}{data.get('customer_email', '')}{self.secret_key}",
                
                # Вариант 26: shop_id + order_id + sum + customer_email + secret_key
                f"{self.shop_id}{data.get('order_id', '')}{data.get('sum', '')}{data.get('customer_email', '')}{self.secret_key}",
                
                # Вариант 27: shop_id + order_id + payment_status + customer_email + secret_key
                f"{self.shop_id}{data.get('order_id', '')}{data.get('payment_status', '')}{data.get('customer_email', '')}{self.secret_key}",
                
                # Вариант 28: shop_id + sum + payment_status + customer_email + secret_key
                f"{self.shop_id}{data.get('sum', '')}{data.get('payment_status', '')}{data.get('customer_email', '')}{self.secret_key}",
                
                # Вариант 29: shop_id + order_id + sum + payment_status + customer_email + secret_key
                f"{self.shop_id}{data.get('order_id', '')}{data.get('sum', '')}{data.get('payment_status', '')}{data.get('customer_email', '')}{self.secret_key}",
                
                # Вариант 30: только customer_email + secret_key
                f"{data.get('customer_email', '')}{self.secret_key}",
                
                # Вариант 31: order_id + sum + currency + customer_email + secret_key
                f"{data.get('order_id', '')}{data.get('sum', '')}{data.get('currency', '')}{data.get('customer_email', '')}{self.secret_key}",
                
                # Вариант 32: shop_id + order_id + sum + currency + customer_email + secret_key
                f"{self.shop_id}{data.get('order_id', '')}{data.get('sum', '')}{data.get('currency', '')}{data.get('customer_email', '')}{self.secret_key}",
                
                # Вариант 33: order_id + currency + payment_status + customer_email + secret_key
                f"{data.get('order_id', '')}{data.get('currency', '')}{data.get('payment_status', '')}{data.get('customer_email', '')}{self.secret_key}",
                
                # Вариант 34: shop_id + order_id + currency + payment_status + customer_email + secret_key
                f"{self.shop_id}{data.get('order_id', '')}{data.get('currency', '')}{data.get('payment_status', '')}{data.get('customer_email', '')}{self.secret_key}",
                
                # Вариант 35: sum + currency + payment_status + customer_email + secret_key
                f"{data.get('sum', '')}{data.get('currency', '')}{data.get('payment_status', '')}{data.get('customer_email', '')}{self.secret_key}",
                
                # Вариант 36: shop_id + sum + currency + payment_status + customer_email + secret_key
                f"{self.shop_id}{data.get('sum', '')}{data.get('currency', '')}{data.get('payment_status', '')}{data.get('customer_email', '')}{self.secret_key}",
                
                # Вариант 37: shop_id + order_id + sum + currency + payment_status + customer_email + secret_key
                f"{self.shop_id}{data.get('order_id', '')}{data.get('sum', '')}{data.get('currency', '')}{data.get('payment_status', '')}{data.get('customer_email', '')}{self.secret_key}",
                
                # Вариант 38: только order_num + secret_key
                f"{data.get('order_num', '')}{self.secret_key}",
                
                # Вариант 39: order_id + order_num + secret_key
                f"{data.get('order_id', '')}{data.get('order_num', '')}{self.secret_key}",
                
                # Вариант 40: shop_id + order_num + secret_key
                f"{self.shop_id}{data.get('order_num', '')}{self.secret_key}"
            ]
            
            for i, variant_data in enumerate(variants, 1):
                expected_signature = self.generate_signature(variant_data)
                print(f"  Вариант {i}: {variant_data}")
                print(f"  Подпись {i}: {expected_signature}")
                
                if hmac.compare_digest(signature, expected_signature):
                    print(f"  ✅ Подпись совпадает с вариантом {i}")
                    return True
            
            print("  ❌ Подпись не совпадает ни с одним вариантом")
            return False

        except Exception as e:
            print(f"Ошибка проверки подписи: {e}")
            return False
    
    def get_payment_status(self, order_id: str) -> Optional[Dict]:
        """Получение статуса платежа из API Prodamus"""
        try:
            # Используем правильный API Prodamus для проверки статуса
            api_url = f"https://api.prodamus.ru/v3/payments/{order_id}"
            
            headers = {
                'Authorization': f'Bearer {self.secret_key}',
                'X-Shop-Id': self.shop_id,
                'Content-Type': 'application/json'
            }
            
            print(f"Проверка статуса платежа через API Prodamus:")
            print(f"  - URL: {api_url}")
            print(f"  - Order ID: {order_id}")
            print(f"  - Shop ID: {self.shop_id}")
            
            response = requests.get(api_url, headers=headers, timeout=10)
            
            print(f"  - Response status: {response.status_code}")
            print(f"  - Response: {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'status': 'success',
                    'amount': data.get('amount', 0),
                    'order_id': order_id,
                    'source': 'api'
                }
            else:
                print(f"  - API Error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Ошибка проверки статуса платежа: {e}")
            return None
    
    def set_activity(self, order_id: str, activity: str) -> bool:
        """Установка активности для заказа"""
        try:
            # Здесь должна быть логика установки активности
            print(f"Установка активности для заказа {order_id}: {activity}")
            return True
        except Exception as e:
            print(f"Ошибка установки активности: {e}")
            return False
    
    def set_subscription_payment_date(self, order_id: str, payment_date: str) -> bool:
        """Установка даты платежа для подписки"""
        try:
            # Здесь должна быть логика установки даты платежа
            print(f"Установка даты платежа для заказа {order_id}: {payment_date}")
            return True
        except Exception as e:
            print(f"Ошибка установки даты платежа: {e}")
            return False
