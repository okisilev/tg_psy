#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Официальная библиотека Hmac для Prodamus
Основана на документации: https://help.prodamus.ru/payform/integracii/rest-api/instrukcii-dlya-samostoyatelnaya-integracii-servisov
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
            if key != 'signature':  # Исключаем поле signature
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
            # Создаем ожидаемую подпись
            expected_signature = Hmac.create(data, secret_key)
            
            # Сравниваем подписи безопасным способом
            return hmac.compare_digest(received_signature, expected_signature)
            
        except Exception as e:
            print(f"Ошибка проверки подписи: {e}")
            return False
    
    @staticmethod
    def create_webhook_signature(data: Dict[str, Any], secret_key: str) -> str:
        """
        Создание подписи для webhook (специальный метод для webhook)
        
        Args:
            data: Данные webhook
            secret_key: Секретный ключ
            
        Returns:
            Подпись в виде hex-строки
        """
        # Для webhook используем специальный алгоритм
        # Сортируем ключи и формируем строку
        sorted_keys = sorted(data.keys())
        
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
