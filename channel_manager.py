import logging
from telegram import Bot
from telegram.error import TelegramError
from config import BOT_TOKEN, CHANNEL_ID, CHANNEL_USERNAME

logger = logging.getLogger(__name__)

class ChannelManager:
    def __init__(self):
        self.bot = Bot(token=BOT_TOKEN)
        self.channel_id = CHANNEL_ID
    
    async def add_user_to_channel(self, user_id: int) -> bool:
        """
        Добавление пользователя в канал
        
        Args:
            user_id: ID пользователя Telegram
            
        Returns:
            bool: True если пользователь успешно добавлен
        """
        try:
            # Приглашаем пользователя в канал
            await self.bot.ban_chat_member(
                chat_id=self.channel_id,
                user_id=user_id
            )
            
            # Разбаниваем пользователя (это добавляет его в канал)
            await self.bot.unban_chat_member(
                chat_id=self.channel_id,
                user_id=user_id
            )
            
            logger.info(f"✅ Пользователь {user_id} добавлен в канал {self.channel_id}")
            return True
            
        except TelegramError as e:
            logger.error(f"❌ Ошибка добавления пользователя {user_id} в канал: {e}")
            
            # Если пользователь уже в канале, считаем это успехом
            if "user is already a participant" in str(e).lower():
                logger.info(f"ℹ️ Пользователь {user_id} уже в канале")
                return True
            
            return False
    
    async def remove_user_from_channel(self, user_id: int) -> bool:
        """
        Удаление пользователя из канала
        
        Args:
            user_id: ID пользователя Telegram
            
        Returns:
            bool: True если пользователь успешно удален
        """
        try:
            # Баним пользователя (удаляем из канала)
            await self.bot.ban_chat_member(
                chat_id=self.channel_id,
                user_id=user_id
            )
            
            logger.info(f"✅ Пользователь {user_id} удален из канала {self.channel_id}")
            return True
            
        except TelegramError as e:
            logger.error(f"❌ Ошибка удаления пользователя {user_id} из канала: {e}")
            
            # Если пользователя нет в канале, считаем это успехом
            if "user not found" in str(e).lower() or "chat member not found" in str(e).lower():
                logger.info(f"ℹ️ Пользователь {user_id} не был в канале")
                return True
            
            return False
    
    async def check_user_in_channel(self, user_id: int) -> bool:
        """
        Проверка, находится ли пользователь в канале
        
        Args:
            user_id: ID пользователя Telegram
            
        Returns:
            bool: True если пользователь в канале
        """
        try:
            member = await self.bot.get_chat_member(
                chat_id=self.channel_id,
                user_id=user_id
            )
            
            # Проверяем статус участника
            status = member.status
            if status in ['member', 'administrator', 'creator']:
                logger.info(f"✅ Пользователь {user_id} находится в канале (статус: {status})")
                return True
            else:
                logger.info(f"ℹ️ Пользователь {user_id} не в канале (статус: {status})")
                return False
                
        except TelegramError as e:
            logger.error(f"❌ Ошибка проверки пользователя {user_id} в канале: {e}")
            return False
    
    async def get_channel_info(self) -> dict:
        """
        Получение информации о канале
        
        Returns:
            dict: Информация о канале
        """
        try:
            chat = await self.bot.get_chat(self.channel_id)
            
            info = {
                'id': chat.id,
                'title': chat.title,
                'username': chat.username,
                'type': chat.type,
                'member_count': getattr(chat, 'member_count', 'Неизвестно')
            }
            
            logger.info(f"✅ Информация о канале получена: {info}")
            return info
            
        except TelegramError as e:
            logger.error(f"❌ Ошибка получения информации о канале: {e}")
            return {}
    
    async def send_message_to_channel(self, message: str, parse_mode: str = None) -> bool:
        """
        Отправка сообщения в канал
        
        Args:
            message: Текст сообщения
            parse_mode: Режим парсинга (HTML, Markdown)
            
        Returns:
            bool: True если сообщение отправлено
        """
        try:
            await self.bot.send_message(
                chat_id=self.channel_id,
                text=message,
                parse_mode=parse_mode
            )
            
            logger.info(f"✅ Сообщение отправлено в канал {self.channel_id}")
            return True
            
        except TelegramError as e:
            logger.error(f"❌ Ошибка отправки сообщения в канал: {e}")
            return False
    
    async def send_welcome_message(self, user_id: int, username: str = None) -> bool:
        """
        Отправка приветственного сообщения в канал при добавлении пользователя
        
        Args:
            user_id: ID пользователя
            username: Username пользователя
            
        Returns:
            bool: True если сообщение отправлено
        """
        try:
            user_mention = f"@{username}" if username else f"ID:{user_id}"
            welcome_text = f"🎉 Добро пожаловать в Женский клуб, {user_mention}!\n\nТеперь у вас есть доступ ко всем материалам и общению в нашем закрытом сообществе."
            
            return await self.send_message_to_channel(welcome_text)
            
        except Exception as e:
            logger.error(f"❌ Ошибка отправки приветственного сообщения: {e}")
            return False
    
    async def send_subscription_expired_notification(self, user_id: int, username: str = None) -> bool:
        """
        Отправка уведомления в канал об истечении подписки пользователя
        
        Args:
            user_id: ID пользователя
            username: Username пользователя
            
        Returns:
            bool: True если уведомление отправлено
        """
        try:
            user_mention = f"@{username}" if username else f"ID:{user_id}"
            notification_text = f"👋 {user_mention} покинул(а) Женский клуб из-за истечения подписки.\n\nДля возвращения оформите новую подписку!"
            
            return await self.send_message_to_channel(notification_text)
            
        except Exception as e:
            logger.error(f"❌ Ошибка отправки уведомления об истечении подписки: {e}")
            return False
