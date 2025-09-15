import asyncio
import logging
from datetime import datetime, timedelta
from config import REMINDER_DAYS_BEFORE

logger = logging.getLogger(__name__)

class SubscriptionScheduler:
    def __init__(self, bot_instance):
        self.bot = bot_instance
        self.is_running = False
    
    async def start(self):
        """Запуск планировщика"""
        self.is_running = True
        logger.info("Планировщик подписок запущен")
        
        # Запускаем задачи в фоне
        asyncio.create_task(self.check_expiring_subscriptions())
        asyncio.create_task(self.check_expired_subscriptions())
    
    async def stop(self):
        """Остановка планировщика"""
        self.is_running = False
        logger.info("Планировщик подписок остановлен")
    
    async def check_expiring_subscriptions(self):
        """Проверка подписок, которые скоро истекают"""
        while self.is_running:
            try:
                # Получаем подписки, которые истекают через 3 дня
                expiring_subscriptions = self.bot.db.get_expiring_subscriptions(REMINDER_DAYS_BEFORE)
                
                for subscription in expiring_subscriptions:
                    user_id = subscription[1]
                    end_date = datetime.strptime(subscription[5], '%Y-%m-%d %H:%M:%S')
                    days_left = (end_date - datetime.now()).days
                    
                    # Отправляем напоминание
                    await self.bot.send_expiry_reminder(user_id, days_left)
                    
                    logger.info(f"Напоминание отправлено пользователю {user_id}, дней до истечения: {days_left}")
                
                # Проверяем каждые 24 часа
                await asyncio.sleep(24 * 60 * 60)
                
            except Exception as e:
                logger.error(f"Ошибка в проверке истекающих подписок: {e}")
                await asyncio.sleep(60)  # Ждем минуту при ошибке
    
    async def check_expired_subscriptions(self):
        """Проверка истекших подписок"""
        while self.is_running:
            try:
                # Получаем истекшие подписки
                expired_subscriptions = self.bot.db.get_expired_subscriptions()
                
                for subscription in expired_subscriptions:
                    user_id = subscription[1]
                    user_info = (user_id, subscription[7], subscription[8])  # user_id, username, first_name
                    
                    # Обрабатываем истекшую подписку
                    await self.bot.handle_expired_subscription(user_id, user_info)
                    
                    logger.info(f"Обработана истекшая подписка пользователя {user_id}")
                
                # Проверяем каждые 6 часов
                await asyncio.sleep(6 * 60 * 60)
                
            except Exception as e:
                logger.error(f"Ошибка в проверке истекших подписок: {e}")
                await asyncio.sleep(60)  # Ждем минуту при ошибке
