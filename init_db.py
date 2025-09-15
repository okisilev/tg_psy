#!/usr/bin/env python3
"""
Скрипт для инициализации базы данных
"""

import logging
from database import Database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_database():
    """Инициализация базы данных"""
    try:
        logger.info("Инициализация базы данных...")
        
        db = Database()
        
        # Создаем таблицы
        db.create_tables()
        
        logger.info("✅ База данных успешно инициализирована")
        
        # Проверяем структуру таблиц
        cursor = db.conn.cursor()
        
        # Проверяем таблицу пользователей
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if cursor.fetchone():
            logger.info("✅ Таблица 'users' создана")
        
        # Проверяем таблицу подписок
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='subscriptions'")
        if cursor.fetchone():
            logger.info("✅ Таблица 'subscriptions' создана")
        
        # Проверяем таблицу платежей
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='payments'")
        if cursor.fetchone():
            logger.info("✅ Таблица 'payments' создана")
        
        db.close()
        
    except Exception as e:
        logger.error(f"❌ Ошибка инициализации базы данных: {e}")
        raise

if __name__ == "__main__":
    init_database()
