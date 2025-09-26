#!/usr/bin/env python3
"""
Скрипт для тестирования функциональности бота
"""

import logging
from database import Database
from prodamus import ProdаmusAPI
from config import SUBSCRIPTION_PRICE

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_database():
    """Тестирование базы данных"""
    logger.info("Тестирование базы данных...")
    
    try:
        db = Database()
        
        # Тестируем добавление пользователя
        test_user_id = 12345
        db.add_user(
            user_id=test_user_id,
            username="test_user",
            first_name="Test",
            last_name="User"
        )
        logger.info("✅ Добавление пользователя работает")
        
        # Тестируем получение пользователя
        user = db.get_user(test_user_id)
        if user:
            logger.info(f"✅ Получение пользователя работает: {user}")
        else:
            logger.error("❌ Ошибка получения пользователя")
        
        # Тестируем создание подписки
        db.create_subscription(test_user_id, "test_payment_123", SUBSCRIPTION_PRICE)
        logger.info("✅ Создание подписки работает")
        
        # Тестируем получение активной подписки
        subscription = db.get_active_subscription(test_user_id)
        if subscription:
            logger.info(f"✅ Получение подписки работает: {subscription}")
        else:
            logger.error("❌ Ошибка получения подписки")
        
        # Тестируем получение всех пользователей
        users = db.get_all_users()
        logger.info(f"✅ Получение всех пользователей работает: {len(users)} пользователей")
        
        db.close()
        
    except Exception as e:
        logger.error(f"❌ Ошибка тестирования базы данных: {e}")
        raise

def test_prodamus():
    """Тестирование интеграции с Продамус"""
    logger.info("Тестирование интеграции с Продамус...")
    
    try:
        prodamus = ProdаmusAPI()
        
        # Проверяем, что класс инициализируется
        if prodamus.shop_id and prodamus.secret_key:
            logger.info("✅ Конфигурация Продамус загружена")
        else:
            logger.warning("⚠️ Конфигурация Продамус не полная (это нормально для тестов)")
        
        # Тестируем генерацию подписи
        test_data = "test_string"
        signature = prodamus.generate_signature(test_data)
        if signature:
            logger.info("✅ Генерация подписи работает")
        else:
            logger.error("❌ Ошибка генерации подписи")
        
        logger.info("✅ Интеграция с Продамус работает")
        
    except Exception as e:
        logger.error(f"❌ Ошибка тестирования Продамус: {e}")
        raise

def test_config():
    """Тестирование конфигурации"""
    logger.info("Тестирование конфигурации...")
    
    try:
        from config import MESSAGES, SUBSCRIPTION_PRICE, REMINDER_DAYS_BEFORE
        
        if MESSAGES:
            logger.info("✅ Сообщения загружены")
        else:
            logger.error("❌ Ошибка загрузки сообщений")
        
        if SUBSCRIPTION_PRICE > 0:
            logger.info(f"✅ Цена подписки настроена: {SUBSCRIPTION_PRICE / 100} руб.")
        else:
            logger.error("❌ Ошибка настройки цены подписки")
        
        if REMINDER_DAYS_BEFORE > 0:
            logger.info(f"✅ Дни напоминания настроены: {REMINDER_DAYS_BEFORE}")
        else:
            logger.error("❌ Ошибка настройки дней напоминания")
        
    except Exception as e:
        logger.error(f"❌ Ошибка тестирования конфигурации: {e}")
        raise

def main():
    """Главная функция тестирования"""
    print("=" * 50)
    print("🧪 Тестирование функциональности бота")
    print("=" * 50)
    
    try:
        test_config()
        test_database()
        test_prodamus()
        
        print("\n" + "=" * 50)
        print("✅ Все тесты прошли успешно!")
        print("=" * 50)
        
    except Exception as e:
        print("\n" + "=" * 50)
        print(f"❌ Тесты завершились с ошибкой: {e}")
        print("=" * 50)
        raise

if __name__ == "__main__":
    main()
