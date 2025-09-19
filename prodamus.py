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
    PRODAMUS_DEMO_MODE,
    PRODAMUS_WEBHOOK_URL,
    SUBSCRIPTION_PRICE
)

class ProdаmusAPI:
    def __init__(self):
        self.shop_id = PRODAMUS_SHOP_ID
        self.secret_key = PRODAMUS_SECRET_KEY
        self.api_url = PRODAMUS_API_URL
        self.demo_mode = PRODAMUS_DEMO_MODE
    
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
            order_id = f'women_club_{user_id}_{int(time.time())}'
            
            # Создаем параметры для URL
            params = {
                'shop_id': self.shop_id,
                'amount': SUBSCRIPTION_PRICE,
                'currency': 'RUB',
                'order_id': order_id,
                'customer_phone': '',
                'customer_email': '',
                'description': 'Подписка на Женский клуб на 1 месяц',
                'success_url': 'https://t.me/your_bot_username',  # Замените на реальный username бота
                'fail_url': 'https://t.me/your_bot_username',     # Замените на реальный username бота
                'callback_url': PRODAMUS_WEBHOOK_URL,  # URL для webhook уведомлений
                'custom_fields': f'user_id:{user_id},username:{username or ""}'
            }
            
            # Добавляем демо-режим если включен
            if self.demo_mode:
                params['demo_mode'] = 1
            
            # Создаем строку для подписи
            sign_string = f"{params['shop_id']}{params['amount']}{params['order_id']}{params['currency']}{self.secret_key}"
            params['signature'] = self.generate_signature(sign_string)
            
            print(f"Создание платежа для пользователя {user_id}")
            print(f"Order ID: {order_id}")
            print(f"Amount: {SUBSCRIPTION_PRICE} копеек")
            print(f"Demo Mode: {self.demo_mode}")
            
            # Создаем URL для платежа
            base_url = "https://dashastar.payform.ru/"
            payment_url = base_url + "?" + "&".join([f"{k}={v}" for k, v in params.items() if v])
            
            print(f"Payment URL: {payment_url}")
            
            return {
                'payment_id': order_id,
                'payment_url': payment_url,
                'amount': SUBSCRIPTION_PRICE
            }
            
        except Exception as e:
            print(f"Ошибка создания платежа: {e}")
            return None
    
    def verify_webhook(self, data: Dict, signature: str) -> bool:
        """Проверка подписи webhook от Продамус"""
        try:
            # Создаем строку для проверки подписи на основе данных от Prodamus
            # Формат: shop_id + order_id + sum + currency + payment_status + secret_key
            sign_data = f"{self.shop_id}{data.get('order_id', '')}{data.get('sum', '')}{data.get('currency', '')}{data.get('payment_status', '')}{self.secret_key}"
            expected_signature = self.generate_signature(sign_data)
            
            print(f"Проверка подписи:")
            print(f"  Данные для подписи: {sign_data}")
            print(f"  Полученная подпись: {signature}")
            print(f"  Ожидаемая подпись: {expected_signature}")
            
            return hmac.compare_digest(signature, expected_signature)
        except Exception as e:
            print(f"Ошибка проверки подписи: {e}")
            return False
    
    def get_payment_status(self, order_id: str) -> Optional[Dict]:
        """Получение статуса платежа из API Prodamus"""
        try:
            # Используем API Prodamus для проверки статуса
            url = "https://secure.payform.ru/status"
            
            # Создаем подпись для запроса
            sign_data = f"{self.shop_id}{order_id}{self.secret_key}"
            signature = self.generate_signature(sign_data)
            
            # Параметры запроса
            params = {
                'shop_id': self.shop_id,
                'order_id': order_id,
                'signature': signature
            }
            
            print(f"🔍 Проверка статуса платежа через API Prodamus:")
            print(f"   - URL: {url}")
            print(f"   - Order ID: {order_id}")
            print(f"   - Shop ID: {self.shop_id}")
            print(f"   - Signature: {signature}")
            
            # Отправляем GET запрос
            response = requests.get(url, params=params, timeout=30)
            
            print(f"   - Response status: {response.status_code}")
            print(f"   - Response text: {response.text}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"   - API Response: {data}")
                    return data
                except ValueError:
                    # Если ответ не JSON, возвращаем None
                    print(f"   - Неверный формат ответа: {response.text}")
                    return None
            else:
                print(f"   - Ошибка API: {response.status_code}")
                return None
            
        except Exception as e:
            print(f"Ошибка получения статуса платежа: {e}")
            return None
    
    def set_activity(self, order_id: str, activity: str) -> bool:
        """Установка активности заказа (setactivity API)"""
        try:
            url = "https://secure.payform.ru/setactivity"
            data = {
                'shop_id': self.shop_id,
                'order_id': order_id,
                'activity': activity,
                'signature': self.generate_signature(f"{self.shop_id}{order_id}{activity}{self.secret_key}")
            }
            
            response = requests.post(url, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result.get('status') == 'success'
            
            return False
            
        except Exception as e:
            print(f"Ошибка установки активности: {e}")
            return False
    
    def set_subscription_payment_date(self, order_id: str, payment_date: str) -> bool:
        """Установка даты платежа для подписки (setsubscriptionpaymentdate API)"""
        try:
            url = "https://secure.payform.ru/setsubscriptionpaymentdate"
            data = {
                'shop_id': self.shop_id,
                'order_id': order_id,
                'payment_date': payment_date,
                'signature': self.generate_signature(f"{self.shop_id}{order_id}{payment_date}{self.secret_key}")
            }
            
            response = requests.post(url, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result.get('status') == 'success'
            
            return False
            
        except Exception as e:
            print(f"Ошибка установки даты платежа подписки: {e}")
            return False
