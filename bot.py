import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, 
    MessageHandler, filters, ContextTypes
)
from telegram.error import TelegramError
from telegram.constants import ParseMode

from config import (
    BOT_TOKEN, ADMIN_CHAT_ID, CHANNEL_ID, CHANNEL_USERNAME,
    MESSAGES, SUBSCRIPTION_PRICE
)
from database import Database
from prodamus import ProdаmusAPI
from scheduler import SubscriptionScheduler
from admin_panel import AdminPanel
from channel_manager import ChannelManager

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class WomenClubBot:
    def __init__(self):
        self.db = Database()
        self.prodamus = ProdаmusAPI()
        self.scheduler = SubscriptionScheduler(self)
        self.admin_panel = AdminPanel(self)
        self.channel_manager = ChannelManager()
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        user = update.effective_user
        user_id = user.id
        
        # Добавляем пользователя в базу данных
        self.db.add_user(
            user_id=user_id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name
        )
        
        # Проверяем активную подписку
        subscription = self.db.get_active_subscription(user_id)
        
        if subscription:
            # У пользователя есть активная подписка
            keyboard = [
                [InlineKeyboardButton("🔗 Перейти в канал", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")]
            ]
            
            # Добавляем кнопку админ-панели для администраторов
            if str(user_id) == ADMIN_CHAT_ID:
                keyboard.append([InlineKeyboardButton("🔧 Админ-панель", callback_data="admin_panel")])
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                "✅ У вас есть активная подписка на Женский клуб!\n\n"
                f"Подписка действует до: {subscription[5][:10]}",
                reply_markup=reply_markup
            )
        else:
            # Предлагаем оформить подписку
            keyboard = [
                [InlineKeyboardButton("💳 Оплатить подписку", callback_data="pay_subscription")]
            ]
            
            # Добавляем кнопку админ-панели для администраторов
            if str(user_id) == ADMIN_CHAT_ID:
                keyboard.append([InlineKeyboardButton("🔧 Админ-панель", callback_data="admin_panel")])
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                MESSAGES['welcome'],
                reply_markup=reply_markup
            )
    
    async def pay_subscription_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик кнопки оплаты подписки"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        
        # Создаем платеж в Продамус
        payment = self.prodamus.create_payment(
            user_id=user_id,
            username=query.from_user.username
        )
        
        if payment:
            # Сохраняем платеж в базу данных
            self.db.add_payment(
                user_id=user_id,
                payment_id=payment['payment_id'],
                amount=payment['amount'],
                status='pending'
            )
            
            keyboard = [
                [InlineKeyboardButton("💳 Оплатить", url=payment['payment_url'])],
                [InlineKeyboardButton("🔄 Проверить оплату", callback_data=f"check_payment_{payment['payment_id']}")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                f"💳 Оплата подписки\n\n"
                f"Сумма: {SUBSCRIPTION_PRICE / 100} руб.\n"
                f"Длительность: 30 дней\n\n"
                f"Нажмите кнопку ниже для перехода к оплате:",
                reply_markup=reply_markup
            )
        else:
            await query.edit_message_text(
                "❌ Ошибка создания платежа. Попробуйте позже или обратитесь к администратору."
            )
    
    async def check_payment_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик проверки оплаты"""
        query = update.callback_query
        await query.answer()
        
        payment_id = query.data.replace("check_payment_", "")
        user_id = query.from_user.id
        
        # Проверяем статус платежа
        payment_status = self.prodamus.get_payment_status(payment_id)
        
        if payment_status and payment_status.get('status') == 'success':
            # Платеж успешен
            await self.activate_subscription(user_id, payment_id, payment_status['amount'])
        else:
            # Платеж еще не прошел
            keyboard = [
                [InlineKeyboardButton("🔄 Проверить снова", callback_data=f"check_payment_{payment_id}")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                "⏳ Платеж еще не поступил.\n\nПопробуйте проверить через несколько минут.",
                reply_markup=reply_markup
            )
    
    async def activate_subscription(self, user_id: int, payment_id: str, amount: int):
        """Активация подписки после успешной оплаты"""
        try:
            # Создаем подписку
            self.db.create_subscription(user_id, payment_id, amount)
            
            # Обновляем статус платежа
            self.db.add_payment(user_id, payment_id, amount, 'success')
            
            # Добавляем пользователя в канал
            success = await self.channel_manager.add_user_to_channel(user_id)
            if success:
                # Отправляем приветственное сообщение в канал
                user_info = self.db.get_user(user_id)
                username = user_info[1] if user_info else None
                await self.channel_manager.send_welcome_message(user_id, username)
            
            # Получаем информацию о пользователе
            user = self.db.get_user(user_id)
            subscription = self.db.get_active_subscription(user_id)
            
            # Уведомляем пользователя
            keyboard = [
                [InlineKeyboardButton("🔗 Перейти в канал", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await self.send_message_to_user(
                user_id,
                MESSAGES['payment_success'],
                reply_markup=reply_markup
            )
            
            # Уведомляем администратора
            await self.notify_admin_payment(user, subscription)
            
        except Exception as e:
            logger.error(f"Ошибка активации подписки: {e}")
    
    async def add_user_to_channel(self, user_id: int):
        """Добавление пользователя в канал"""
        return await self.channel_manager.add_user_to_channel(user_id)
    
    async def remove_user_from_channel(self, user_id: int):
        """Удаление пользователя из канала"""
        return await self.channel_manager.remove_user_from_channel(user_id)
    
    async def send_message_to_user(self, user_id: int, text: str, reply_markup=None):
        """Отправка сообщения пользователю"""
        try:
            # Отправляем сообщение через бота
            await self.channel_manager.bot.send_message(
                chat_id=user_id,
                text=text,
                reply_markup=reply_markup
            )
            logger.info(f"✅ Сообщение отправлено пользователю {user_id}")
            
        except Exception as e:
            logger.error(f"❌ Ошибка отправки сообщения пользователю {user_id}: {e}")
    
    async def notify_admin_payment(self, user, subscription):
        """Уведомление администратора о новом платеже"""
        try:
            message = MESSAGES['admin_payment_notification'].format(
                username=user[1] or 'Не указан',
                user_id=user[0],
                amount=subscription[3] / 100,
                expiry_date=subscription[5][:10]
            )
            
            # Отправляем уведомление администратору
            await self.channel_manager.bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                text=message
            )
            logger.info(f"✅ Уведомление администратору отправлено: {message}")
            
        except Exception as e:
            logger.error(f"❌ Ошибка уведомления администратора: {e}")
    
    async def notify_admin_removal(self, user):
        """Уведомление администратора об удалении пользователя"""
        try:
            message = MESSAGES['admin_removal_notification'].format(
                username=user[1] or 'Не указан',
                user_id=user[0]
            )
            
            # Отправляем уведомление администратору
            await self.channel_manager.bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                text=message
            )
            logger.info(f"✅ Уведомление администратору отправлено: {message}")
            
        except Exception as e:
            logger.error(f"❌ Ошибка уведомления администратора: {e}")
    
    async def send_expiry_reminder(self, user_id: int, days_left: int):
        """Отправка напоминания об истечении подписки"""
        try:
            keyboard = [
                [InlineKeyboardButton("💳 Продлить подписку", callback_data="pay_subscription")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            message = MESSAGES['subscription_ending'].format(days=days_left)
            
            await self.send_message_to_user(user_id, message, reply_markup)
            
        except Exception as e:
            logger.error(f"Ошибка отправки напоминания: {e}")
    
    async def handle_expired_subscription(self, user_id: int, user_info):
        """Обработка истекшей подписки"""
        try:
            # Удаляем пользователя из канала
            await self.remove_user_from_channel(user_id)
            
            # Отправляем уведомление в канал об уходе пользователя
            username = user_info[1] if user_info else None
            await self.channel_manager.send_subscription_expired_notification(user_id, username)
            
            # Деактивируем подписку
            self.db.deactivate_subscription(user_id)
            
            # Уведомляем пользователя
            keyboard = [
                [InlineKeyboardButton("💳 Оформить подписку", callback_data="pay_subscription")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await self.send_message_to_user(
                user_id,
                MESSAGES['subscription_expired'],
                reply_markup
            )
            
            # Уведомляем администратора
            await self.notify_admin_removal(user_info)
            
        except Exception as e:
            logger.error(f"Ошибка обработки истекшей подписки: {e}")
    
    async def admin_panel_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Админ-панель"""
        user_id = update.effective_user.id
        
        # Проверяем, является ли пользователь администратором
        if str(user_id) != ADMIN_CHAT_ID:
            await update.message.reply_text("❌ У вас нет прав доступа к админ-панели.")
            return
        
        keyboard = [
            [InlineKeyboardButton("📊 Отчет по платежам", callback_data="admin_report")],
            [InlineKeyboardButton("👥 Пользователи", callback_data="admin_users")],
            [InlineKeyboardButton("🔄 Проверить подписки", callback_data="admin_check_subscriptions")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "🔧 Админ-панель Женского клуба\n\nВыберите действие:",
            reply_markup=reply_markup
        )
    
    async def admin_panel_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик кнопки админ-панели"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        
        # Проверяем, является ли пользователь администратором
        if str(user_id) != ADMIN_CHAT_ID:
            await query.edit_message_text("❌ У вас нет прав доступа к админ-панели.")
            return
        
        keyboard = [
            [InlineKeyboardButton("📊 Отчет по платежам", callback_data="admin_report")],
            [InlineKeyboardButton("👥 Пользователи", callback_data="admin_users")],
            [InlineKeyboardButton("🔄 Проверить подписки", callback_data="admin_check_subscriptions")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "🔧 Админ-панель Женского клуба\n\nВыберите действие:",
            reply_markup=reply_markup
        )
    
    async def main_menu_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Возврат в главное меню"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        
        # Проверяем активную подписку
        subscription = self.db.get_active_subscription(user_id)
        
        if subscription:
            # У пользователя есть активная подписка
            keyboard = [
                [InlineKeyboardButton("🔗 Перейти в канал", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")]
            ]
            
            # Добавляем кнопку админ-панели для администраторов
            if str(user_id) == ADMIN_CHAT_ID:
                keyboard.append([InlineKeyboardButton("🔧 Админ-панель", callback_data="admin_panel")])
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                "✅ У вас есть активная подписка на Женский клуб!\n\n"
                f"Подписка действует до: {subscription[5][:10]}",
                reply_markup=reply_markup
            )
        else:
            # Предлагаем оформить подписку
            keyboard = [
                [InlineKeyboardButton("💳 Оплатить подписку", callback_data="pay_subscription")]
            ]
            
            # Добавляем кнопку админ-панели для администраторов
            if str(user_id) == ADMIN_CHAT_ID:
                keyboard.append([InlineKeyboardButton("🔧 Админ-панель", callback_data="admin_panel")])
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                MESSAGES['welcome'],
                reply_markup=reply_markup
            )
    
    async def admin_report_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик отчета по платежам"""
        await self.admin_panel.admin_report_callback(update, context)
    
    def setup_handlers(self, application: Application):
        """Настройка обработчиков команд"""
        # Команды
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("admin", self.admin_panel_command))
        
        # Callback handlers
        application.add_handler(CallbackQueryHandler(self.pay_subscription_callback, pattern="^pay_subscription$"))
        application.add_handler(CallbackQueryHandler(self.check_payment_callback, pattern="^check_payment_"))
        application.add_handler(CallbackQueryHandler(self.admin_panel_callback, pattern="^admin_panel$"))
        application.add_handler(CallbackQueryHandler(self.main_menu_callback, pattern="^main_menu$"))
        
        # Админ-панель handlers
        self.admin_panel.setup_admin_handlers(application)
    
    async def start_scheduler(self):
        """Запуск планировщика задач"""
        await self.scheduler.start()
    
    def run(self):
        """Запуск бота"""
        application = Application.builder().token(BOT_TOKEN).build()
        
        self.setup_handlers(application)
        
        # Запускаем планировщик
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.create_task(self.start_scheduler())
        
        # Запускаем бота
        application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    bot = WomenClubBot()
    bot.run()
