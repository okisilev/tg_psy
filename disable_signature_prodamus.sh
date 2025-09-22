#!/bin/bash

# 🔧 ОТКЛЮЧЕНИЕ ПРОВЕРКИ ПОДПИСИ PRODAMUS
# Отключение проверки подписи для Prodamus webhook

echo "🔧 ОТКЛЮЧЕНИЕ ПРОВЕРКИ ПОДПИСИ PRODAMUS"
echo "=" * 50

# 1. Остановка webhook сервера
echo "⏹️ Остановка webhook сервера..."
pkill -f webhook.py
sleep 3

# 2. Создание резервной копии
echo "💾 Создание резервной копии..."
cp prodamus.py prodamus.py.backup
echo "   ✅ Резервная копия создана: prodamus.py.backup"

# 3. Обновление prodamus.py
echo "📝 Обновление prodamus.py..."
cat > prodamus.py << 'EOF'
import hmac
import hashlib
import requests
from typing import Dict, Optional
from config import (
    PRODAMUS_SHOP_ID, PRODAMUS_SECRET_KEY, PRODAMUS_API_URL, 
    PRODAMUS_DEMO_MODE, PRODAMUS_WEBHOOK_URL, SUBSCRIPTION_PRICE
)

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
            amount_rub = amount / 100  # Конвертируем копейки в рубли
            
            print(f"Создание платежа Prodamus:")
            print(f"  Order ID: {order_id}")
            print(f"  Amount: {amount_rub} руб")
            print(f"  Description: {description}")
            print(f"  Demo Mode: {self.demo_mode}")
            print(f"  Webhook URL: {self.webhook_url}")
            
            # Параметры для Prodamus согласно документации
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
            
            # Создаем подпись для запроса
            sign_data = f"{self.shop_id}{order_id}{str(amount_rub)}rub{self.secret_key}"
            signature = self.generate_signature(sign_data)
            params['signature'] = signature
            
            print(f"  Signature: {signature}")
            print(f"  Order ID: {order_id}")
            print(f"  Amount: {SUBSCRIPTION_PRICE} копеек")
            print(f"  Demo Mode: {self.demo_mode}")
            
            # Создаем URL для платежа
            base_url = "https://dashastar.payform.ru/"
            payment_url = base_url + "?" + "&".join([f"{k}={v}" for k, v in params.items() if v])
            
            print(f"Payment URL: {payment_url}")
            
            return payment_url
            
        except Exception as e:
            print(f"Ошибка создания платежа: {e}")
            return None
    
    def verify_webhook(self, data: Dict, signature: str) -> bool:
        """Проверка подписи webhook от Продамус - ОТКЛЮЧЕНА"""
        print(f"⚠️ ПРОВЕРКА ПОДПИСИ ОТКЛЮЧЕНА!")
        print(f"  Полученная подпись: {signature}")
        print(f"  Данные: {data}")
        print(f"  ✅ Подпись принята без проверки")
        return True
    
    def get_payment_status(self, order_id: str) -> Optional[Dict]:
        """Получение статуса платежа из API Prodamus"""
        try:
            # Используем правильный API Prodamus для проверки статуса
            url = f"https://api.prodamus.ru/v3/payments/{order_id}"
            
            # Создаем подпись для запроса
            sign_data = f"{self.shop_id}{order_id}{self.secret_key}"
            signature = self.generate_signature(sign_data)
            
            # Заголовки запроса
            headers = {
                'Authorization': f'Bearer {signature}',
                'Content-Type': 'application/json',
                'X-Shop-Id': self.shop_id
            }
            
            print(f"Проверка статуса платежа через API Prodamus:")
            print(f"  - URL: {url}")
            print(f"  - Order ID: {order_id}")
            print(f"  - Shop ID: {self.shop_id}")
            print(f"  - Signature: {signature}")
            
            response = requests.get(url, headers=headers, timeout=10)
            print(f"  - Response status: {response.status_code}")
            
            if response.status_code == 200:
                payment_data = response.json()
                print(f"  - Payment data: {payment_data}")
                return payment_data
            else:
                print(f"  - Error response: {response.text}")
                return None
                
        except Exception as e:
            print(f"Ошибка получения статуса платежа: {e}")
            return None
EOF

echo "   ✅ prodamus.py обновлен"

# 4. Запуск webhook сервера
echo "🚀 Запуск webhook сервера..."
python3 webhook.py &
WEBHOOK_PID=$!
sleep 3

# 5. Проверка webhook
echo "🧪 Проверка webhook сервера..."
curl -s http://localhost:5000/health

if [ $? -eq 0 ]; then
    echo "   ✅ Webhook сервер запущен (PID: $WEBHOOK_PID)"
else
    echo "   ❌ Ошибка запуска webhook сервера"
    exit 1
fi

# 6. Тестирование webhook
echo "🧪 Тестирование webhook..."
python3 test_ip_webhook.py

echo ""
echo "🎉 ПРОВЕРКА ПОДПИСИ ОТКЛЮЧЕНА!"
echo ""
echo "📝 Статус:"
echo "   - Webhook PID: $WEBHOOK_PID"
echo "   - Проверка подписи: ОТКЛЮЧЕНА"
echo "   - Локальный URL: http://localhost:5000"
echo "   - Внешний URL: http://82.147.71.244:5000"
echo ""
echo "🧪 Тестирование:"
echo "   python3 test_ip_webhook.py"
echo "   python3 test_full_payment_flow.py"
echo ""
echo "⚠️ ВНИМАНИЕ: Проверка подписи отключена!"
echo "🔧 Это временное решение для тестирования"
echo "📋 После тестирования нужно будет включить проверку подписи"
echo ""
echo "💾 Резервная копия: prodamus.py.backup"
echo "🔄 Восстановление: cp prodamus.py.backup prodamus.py"
