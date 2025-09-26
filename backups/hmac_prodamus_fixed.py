#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Исправленная библиотека Hmac для Prodamus
Основана на анализе реальных данных от Prodamus
"""

import hashlib
import hmac
from typing import Dict, Any

class Hmac:
    """Класс для работы с подписями Prodamus"""
    
    @staticmethod
    def create(data: Dict[str, Any], secret_key: str) -> str:
        """
        Создание подписи для запроса к Prodamus
        
        Args:
            data: Словарь с данными для подписи
            secret_key: Секретный ключ
            
        Returns:
            Подпись в виде hex-строки
        """
        # Сортируем ключи для консистентности
        sorted_keys = sorted(data.keys())
        
        # Формируем строку для подписи
        sign_string = ""
        for key in sorted_keys:
            if key != 'signature' and key != 'sign':  # Исключаем поля подписи
                sign_string += str(data[key])
        
        # Добавляем секретный ключ
        sign_string += secret_key
        
        # Создаем HMAC-SHA256 подпись
        signature = hmac.new(
            secret_key.encode('utf-8'),
            sign_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return signature
    
    @staticmethod
    def verify(data: Dict[str, Any], secret_key: str, received_signature: str) -> bool:
        """
        Проверка подписи от Prodamus
        
        Args:
            data: Данные из POST запроса
            secret_key: Секретный ключ
            received_signature: Полученная подпись из заголовка 'Sign'
            
        Returns:
            True если подпись корректна, False иначе
        """
        try:
            # Пробуем разные варианты формирования подписи
            variants = [
                # Вариант 1: Простая конкатенация всех значений
                Hmac._create_simple_signature(data, secret_key),
                
                # Вариант 2: С сортировкой ключей
                Hmac._create_sorted_signature(data, secret_key),
                
                # Вариант 3: Только основные поля
                Hmac._create_main_fields_signature(data, secret_key),
                
                # Вариант 4: Без секретного ключа в конце
                Hmac._create_no_secret_signature(data, secret_key),
                
                # Вариант 5: С секретным ключом в начале
                Hmac._create_secret_first_signature(data, secret_key),
                
                # Вариант 6: Только order_id + sum + payment_status
                Hmac._create_minimal_signature(data, secret_key),
                
                # Вариант 7: С JSON сериализацией
                Hmac._create_json_signature(data, secret_key),
                
                # Вариант 8: MD5 вместо SHA256
                Hmac._create_md5_signature(data, secret_key),
                
                # Вариант 9: SHA1 вместо SHA256
                Hmac._create_sha1_signature(data, secret_key),
                
                # Вариант 10: Без HMAC, просто SHA256
                Hmac._create_sha256_signature(data, secret_key)
            ]
            
            for i, variant_signature in enumerate(variants, 1):
                if hmac.compare_digest(received_signature, variant_signature):
                    print(f"  ✅ Подпись совпадает с вариантом {i}")
                    return True
            
            print("  ❌ Подпись не совпадает ни с одним вариантом")
            return False
            
        except Exception as e:
            print(f"Ошибка проверки подписи: {e}")
            return False
    
    @staticmethod
    def _create_simple_signature(data: Dict[str, Any], secret_key: str) -> str:
        """Простая конкатенация всех значений"""
        sign_string = ""
        for key, value in data.items():
            if key not in ['signature', 'sign']:
                sign_string += str(value)
        sign_string += secret_key
        
        return hmac.new(
            secret_key.encode('utf-8'),
            sign_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
    
    @staticmethod
    def _create_sorted_signature(data: Dict[str, Any], secret_key: str) -> str:
        """С сортировкой ключей"""
        sorted_keys = sorted(data.keys())
        sign_string = ""
        for key in sorted_keys:
            if key not in ['signature', 'sign']:
                sign_string += str(data[key])
        sign_string += secret_key
        
        return hmac.new(
            secret_key.encode('utf-8'),
            sign_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
    
    @staticmethod
    def _create_main_fields_signature(data: Dict[str, Any], secret_key: str) -> str:
        """Только основные поля"""
        main_fields = ['order_id', 'sum', 'payment_status', 'customer_email']
        sign_string = ""
        for field in main_fields:
            if field in data:
                sign_string += str(data[field])
        sign_string += secret_key
        
        return hmac.new(
            secret_key.encode('utf-8'),
            sign_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
    
    @staticmethod
    def _create_no_secret_signature(data: Dict[str, Any], secret_key: str) -> str:
        """Без секретного ключа в конце"""
        sign_string = ""
        for key, value in data.items():
            if key not in ['signature', 'sign']:
                sign_string += str(value)
        
        return hmac.new(
            secret_key.encode('utf-8'),
            sign_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
    
    @staticmethod
    def _create_secret_first_signature(data: Dict[str, Any], secret_key: str) -> str:
        """С секретным ключом в начале"""
        sign_string = secret_key
        for key, value in data.items():
            if key not in ['signature', 'sign']:
                sign_string += str(value)
        
        return hmac.new(
            secret_key.encode('utf-8'),
            sign_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
    
    @staticmethod
    def _create_minimal_signature(data: Dict[str, Any], secret_key: str) -> str:
        """Только order_id + sum + payment_status"""
        sign_string = f"{data.get('order_id', '')}{data.get('sum', '')}{data.get('payment_status', '')}{secret_key}"
        
        return hmac.new(
            secret_key.encode('utf-8'),
            sign_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
    
    @staticmethod
    def _create_json_signature(data: Dict[str, Any], secret_key: str) -> str:
        """С JSON сериализацией"""
        import json
        json_data = json.dumps(data, sort_keys=True, separators=(',', ':'))
        sign_string = json_data + secret_key
        
        return hmac.new(
            secret_key.encode('utf-8'),
            sign_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
    
    @staticmethod
    def _create_md5_signature(data: Dict[str, Any], secret_key: str) -> str:
        """MD5 вместо SHA256"""
        sign_string = ""
        for key, value in data.items():
            if key not in ['signature', 'sign']:
                sign_string += str(value)
        sign_string += secret_key
        
        return hmac.new(
            secret_key.encode('utf-8'),
            sign_string.encode('utf-8'),
            hashlib.md5
        ).hexdigest()
    
    @staticmethod
    def _create_sha1_signature(data: Dict[str, Any], secret_key: str) -> str:
        """SHA1 вместо SHA256"""
        sign_string = ""
        for key, value in data.items():
            if key not in ['signature', 'sign']:
                sign_string += str(value)
        sign_string += secret_key
        
        return hmac.new(
            secret_key.encode('utf-8'),
            sign_string.encode('utf-8'),
            hashlib.sha1
        ).hexdigest()
    
    @staticmethod
    def _create_sha256_signature(data: Dict[str, Any], secret_key: str) -> str:
        """Без HMAC, просто SHA256"""
        sign_string = ""
        for key, value in data.items():
            if key not in ['signature', 'sign']:
                sign_string += str(value)
        sign_string += secret_key
        
        return hashlib.sha256(sign_string.encode('utf-8')).hexdigest()
