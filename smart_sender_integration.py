#!/usr/bin/env python3
"""
Интеграция с Smart Sender API
"""

import requests
import json
import os
from typing import Dict, Optional, List
from datetime import datetime

class SmartSenderAPI:
    def __init__(self, api_key: str = None):
        """
        Инициализация Smart Sender API
        
        Args:
            api_key: API ключ Smart Sender (если не указан, берется из переменных окружения)
        """
        self.api_key = api_key or os.getenv('SMART_SENDER_API_KEY')
        self.base_url = "https://api.smartsender.io"
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
    
    def test_connection(self) -> bool:
        """Тест подключения к Smart Sender API"""
        try:
            url = f"{self.base_url}/v1/contacts"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                print("✅ Подключение к Smart Sender API успешно!")
                return True
            else:
                print(f"❌ Ошибка подключения: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Ошибка подключения к Smart Sender API: {e}")
            return False
    
    def create_contact(self, phone: str, name: str = None, email: str = None, custom_fields: Dict = None) -> Optional[Dict]:
        """
        Создание контакта в Smart Sender
        
        Args:
            phone: Номер телефона
            name: Имя контакта
            email: Email контакта
            custom_fields: Дополнительные поля
            
        Returns:
            Данные созданного контакта или None при ошибке
        """
        try:
            url = f"{self.base_url}/v1/contacts"
            
            data = {
                'phone': phone,
                'name': name,
                'email': email,
                'customFields': custom_fields or {}
            }
            
            response = requests.post(url, json=data, headers=self.headers, timeout=10)
            
            if response.status_code == 201:
                result = response.json()
                print(f"✅ Контакт создан: {result.get('id')}")
                return result
            else:
                print(f"❌ Ошибка создания контакта: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Ошибка создания контакта: {e}")
            return None
    
    def send_message(self, contact_id: str, message: str, message_type: str = "text") -> bool:
        """
        Отправка сообщения контакту
        
        Args:
            contact_id: ID контакта
            message: Текст сообщения
            message_type: Тип сообщения (text, image, etc.)
            
        Returns:
            True если сообщение отправлено успешно
        """
        try:
            url = f"{self.base_url}/v1/contacts/{contact_id}/messages"
            
            data = {
                'type': message_type,
                'content': message
            }
            
            response = requests.post(url, json=data, headers=self.headers, timeout=10)
            
            if response.status_code == 201:
                print(f"✅ Сообщение отправлено контакту {contact_id}")
                return True
            else:
                print(f"❌ Ошибка отправки сообщения: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Ошибка отправки сообщения: {e}")
            return False
    
    def add_to_sequence(self, contact_id: str, sequence_id: str) -> bool:
        """
        Добавление контакта в последовательность
        
        Args:
            contact_id: ID контакта
            sequence_id: ID последовательности
            
        Returns:
            True если контакт добавлен в последовательность
        """
        try:
            url = f"{self.base_url}/v1/sequences/{sequence_id}/contacts"
            
            data = {
                'contactId': contact_id
            }
            
            response = requests.post(url, json=data, headers=self.headers, timeout=10)
            
            if response.status_code == 201:
                print(f"✅ Контакт {contact_id} добавлен в последовательность {sequence_id}")
                return True
            else:
                print(f"❌ Ошибка добавления в последовательность: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Ошибка добавления в последовательность: {e}")
            return False
    
    def get_contact(self, contact_id: str) -> Optional[Dict]:
        """
        Получение информации о контакте
        
        Args:
            contact_id: ID контакта
            
        Returns:
            Данные контакта или None при ошибке
        """
        try:
            url = f"{self.base_url}/v1/contacts/{contact_id}"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Ошибка получения контакта: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Ошибка получения контакта: {e}")
            return None
    
    def update_contact(self, contact_id: str, update_data: Dict) -> bool:
        """
        Обновление данных контакта
        
        Args:
            contact_id: ID контакта
            update_data: Данные для обновления
            
        Returns:
            True если контакт обновлен успешно
        """
        try:
            url = f"{self.base_url}/v1/contacts/{contact_id}"
            response = requests.put(url, json=update_data, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ Контакт {contact_id} обновлен")
                return True
            else:
                print(f"❌ Ошибка обновления контакта: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Ошибка обновления контакта: {e}")
            return False

def test_smart_sender_integration():
    """Тест интеграции с Smart Sender"""
    print("🧪 Тестирование интеграции с Smart Sender...")
    
    # Инициализация API
    api = SmartSenderAPI()
    
    if not api.api_key:
        print("❌ SMART_SENDER_API_KEY не установлен")
        return False
    
    print(f"API Key: {'*' * 20}...{api.api_key[-4:]}")
    
    # Тест подключения
    if not api.test_connection():
        return False
    
    # Тест создания контакта
    test_contact = api.create_contact(
        phone="+79123456789",
        name="Test User",
        email="test@example.com",
        custom_fields={
            "telegram_id": "12345",
            "subscription_status": "active"
        }
    )
    
    if not test_contact:
        return False
    
    contact_id = test_contact.get('id')
    
    # Тест отправки сообщения
    if not api.send_message(contact_id, "Тестовое сообщение от бота"):
        return False
    
    # Тест обновления контакта
    if not api.update_contact(contact_id, {
        "customFields": {
            "telegram_id": "12345",
            "subscription_status": "expired",
            "last_payment": datetime.now().isoformat()
        }
    }):
        return False
    
    print("✅ Все тесты Smart Sender пройдены успешно!")
    return True

if __name__ == "__main__":
    test_smart_sender_integration()
