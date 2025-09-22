import logging
import asyncio
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, 
    MessageHandler, filters, ContextTypes
)
from telegram.error import TelegramError
from telegram.constants import ParseMode

from config import (
    BOT_TOKEN, ADMIN_CHAT_ID, CHANNEL_ID, CHANNEL_USERNAME, CHANNEL_INVITE_LINK,
    WHATSAPP_NUMBER, MESSAGES, SUBSCRIPTION_PRICE
)
from database import Database
from prodamus import ProdаmusAPI
from scheduler import SubscriptionScheduler
from admin_panel import AdminPanel
from channel_manager import ChannelManager
from admin_auth import AdminAuth

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
        self.admin_auth = AdminAuth(self.db)
        
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
                [InlineKeyboardButton("🔗 Перейти в канал", url=CHANNEL_INVITE_LINK)],
                [InlineKeyboardButton("💬 Индивидуальная консультация", callback_data="consultation")]
            ]
            
            # Добавляем кнопку админ-панели для администраторов
            if self.admin_auth.is_admin(user_id):
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
                [InlineKeyboardButton("💳 Оплатить подписку", callback_data="pay_subscription")],
                [InlineKeyboardButton("💬 Индивидуальная консультация", callback_data="consultation")]
            ]
            
            # Добавляем кнопку админ-панели для администраторов
            if self.admin_auth.is_admin(user_id):
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
            order_id=f"women_club_{user_id}_{int(time.time())}",
            amount=5000,  # 50 рублей в копейках
            description="Доступ к обучающим материалам",
            user_id=user_id
        )
        
        if payment:
            # payment - это URL, а не словарь
            payment_id = f"women_club_{user_id}_{int(time.time())}"
            
            # Сохраняем платеж в базу данных
            self.db.add_payment(
                user_id=user_id,
                payment_id=payment_id,
                amount=5000,  # 50 рублей в копейках
                status='pending'
            )
            
            keyboard = [
                [InlineKeyboardButton("💳 Оплатить", url=payment)],
                [InlineKeyboardButton("🔄 Проверить оплату", callback_data=f"check_payment_{payment_id}")]
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
        
        print(f"🔍 Проверка платежа: payment_id={payment_id}, user_id={user_id}")
        

        # Проверяем статус платежа (сначала в базе данных, потом API)
        payment_status = self.get_payment_status_alternative(payment_id)
        
        print(f"📊 Статус платежа: {payment_status}")
        
        # Проверяем статус платежа
        if payment_status and payment_status.get('status') == 'success':
            # Платеж успешен
            print(f"✅ Платеж успешен! Активируем подписку для пользователя {user_id}")
            
            # Получаем сумму из ответа
            amount = payment_status.get('amount', 5000)  # По умолчанию 50 рублей
            await self.activate_subscription(user_id, payment_id, amount)
        else:
            # Платеж еще не прошел - добавляем время проверки для уникальности
            import time
            current_time = time.strftime("%H:%M:%S")
            
            keyboard = [
                [InlineKeyboardButton("🔄 Проверить снова", callback_data=f"check_payment_{payment_id}")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            # Добавляем время проверки для избежания ошибки "Message is not modified"
            message_text = f"⏳ Платеж еще не поступил.\n\nПопробуйте проверить через несколько минут.\n\n🕐 Последняя проверка: {current_time}"
            
            try:
                await query.edit_message_text(
                    message_text,
                    reply_markup=reply_markup
                )
            except Exception as e:
                # Если сообщение не изменилось, просто отвечаем на callback
                print(f"Сообщение не изменилось: {e}")
                await query.answer("Платеж еще не поступил. Попробуйте позже.")
    
    def get_payment_status_alternative(self, order_id: str) -> dict:
        """Альтернативная проверка статуса платежа"""
        try:
            print(f"🔍 Альтернативная проверка статуса платежа: {order_id}")
            
            # 1. Проверяем в базе данных (webhook мог уже сохранить статус)
            cursor = self.db.conn.cursor()
            cursor.execute('''
                SELECT user_id, payment_id, amount, status, created_at
                FROM payments 
                WHERE payment_id = ?
            ''', (order_id,))
            
            result = cursor.fetchone()
            
            if result:
                user_id, payment_id, amount, status, created_at = result
                print(f"   ✅ Платеж найден в базе данных: status={status}")
                return {
                    'status': status,
                    'amount': amount,
                    'user_id': user_id,
                    'created_at': created_at,
                    'source': 'database'
                }
            
            # 2. Если не найден в базе, пробуем API Prodamus
            print(f"   🔍 Платеж не найден в базе, проверяем API Prodamus...")
            
            # Пробуем API Prodamus
            try:
                api_status = self.prodamus.get_payment_status(order_id)
                if api_status:
                    print(f"   ✅ API ответ получен: {api_status}")
                    return api_status
                else:
                    print(f"   ❌ API не вернул данные")
            except Exception as e:
                print(f"   ❌ Ошибка API: {e}")
            
            # 3. Если API не работает, возвращаем None
            print(f"   ❌ Платеж не найден ни в базе, ни в API")
            return None
            
        except Exception as e:
            print(f"Ошибка альтернативной проверки: {e}")
            return None

    async def activate_subscription(self, user_id: int, payment_id: str, amount: int):
        """Активация подписки после успешной оплаты"""
        try:
            # Проверяем, не активирована ли уже подписка
            existing_subscription = self.db.get_active_subscription(user_id)
            if existing_subscription:
                logger.info(f"Подписка для пользователя {user_id} уже активирована")
                return
            
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
                [InlineKeyboardButton("🔗 Перейти в канал", url=CHANNEL_INVITE_LINK)],
                [InlineKeyboardButton("💬 Индивидуальная консультация", callback_data="consultation")]
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
            # Отправляем сообщение об ошибке пользователю
            try:
                await self.send_message_to_user(
                    user_id,
                    "❌ Произошла ошибка при активации подписки. Обратитесь к администратору."
                )
            except Exception as send_error:
                logger.error(f"Ошибка отправки сообщения об ошибке: {send_error}")
    
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
            # Проверяем, что user и subscription не None
            if not user or not subscription:
                logger.error("User или subscription не найдены для уведомления администратора")
                return
            
            # Извлекаем данные безопасно
            username = user[1] if len(user) > 1 and user[1] else 'Не указан'
            user_id = user[0] if len(user) > 0 else 'Неизвестен'
            amount = subscription[3] / 100 if len(subscription) > 3 and subscription[3] else 0
            expiry_date = subscription[5][:10] if len(subscription) > 5 and subscription[5] else 'Неизвестно'
            
            message = MESSAGES['admin_payment_notification'].format(
                username=username,
                user_id=user_id,
                amount=amount,
                expiry_date=expiry_date
            )
            
            # Отправляем уведомление администратору
            await self.channel_manager.bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                text=message
            )
            logger.info(f"✅ Уведомление администратору отправлено: {message}")
            
        except Exception as e:
            logger.error(f"❌ Ошибка уведомления администратора: {e}")
            # Отправляем простое уведомление об ошибке
            try:
                await self.channel_manager.bot.send_message(
                    chat_id=ADMIN_CHAT_ID,
                    text=f"💰 Новый платеж! Пользователь ID: {user[0] if user else 'Неизвестен'}"
                )
            except Exception as send_error:
                logger.error(f"Ошибка отправки простого уведомления: {send_error}")
    
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
        if not self.admin_auth.is_admin(user_id):
            await update.message.reply_text("❌ У вас нет прав доступа к админ-панели.")
            return
        
        keyboard = [
            [InlineKeyboardButton("📊 Отчет по платежам", callback_data="admin_report")],
            [InlineKeyboardButton("👥 Пользователи", callback_data="admin_users")],
            [InlineKeyboardButton("🔄 Проверить подписки", callback_data="admin_check_subscriptions")],
            [InlineKeyboardButton("👑 Администраторы", callback_data="admin_manage_admins")]
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
        if not self.admin_auth.is_admin(user_id):
            await query.edit_message_text("❌ У вас нет прав доступа к админ-панели.")
            return
        
        keyboard = [
            [InlineKeyboardButton("📊 Отчет по платежам", callback_data="admin_report")],
            [InlineKeyboardButton("👥 Пользователи", callback_data="admin_users")],
            [InlineKeyboardButton("🔄 Проверить подписки", callback_data="admin_check_subscriptions")],
            [InlineKeyboardButton("👑 Администраторы", callback_data="admin_manage_admins")]
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
                [InlineKeyboardButton("🔗 Перейти в канал", url=CHANNEL_INVITE_LINK)],
                [InlineKeyboardButton("💬 Индивидуальная консультация", callback_data="consultation")]
            ]
            
            # Добавляем кнопку админ-панели для администраторов
            if self.admin_auth.is_admin(user_id):
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
                [InlineKeyboardButton("💳 Оплатить подписку", callback_data="pay_subscription")],
                [InlineKeyboardButton("💬 Индивидуальная консультация", callback_data="consultation")]
            ]
            
            # Добавляем кнопку админ-панели для администраторов
            if self.admin_auth.is_admin(user_id):
                keyboard.append([InlineKeyboardButton("🔧 Админ-панель", callback_data="admin_panel")])
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                MESSAGES['welcome'],
                reply_markup=reply_markup
            )
    
    async def admin_report_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик отчета по платежам"""
        await self.admin_panel.admin_report_callback(update, context)
    
    async def consultation_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик кнопки индивидуальной консультации"""
        query = update.callback_query
        await query.answer()
        
        # Формируем сообщение с информацией о консультации
        message = MESSAGES['consultation_info'].format(whatsapp_number=WHATSAPP_NUMBER)
        
        # Создаем кнопку для перехода в WhatsApp
        whatsapp_url = f"https://wa.me/{WHATSAPP_NUMBER.replace('+', '')}"
        keyboard = [
            [InlineKeyboardButton("💬 Перейти в WhatsApp", url=whatsapp_url)],
            [InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(message, reply_markup=reply_markup)
    
    async def handle_admin_id_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка сообщения с ID администратора"""
        user_id = update.effective_user.id
        
        # Проверяем, ожидаем ли мы ID администратора
        if not context.user_data.get('waiting_for_admin_id', False):
            return
        
        # Проверяем права супер-администратора
        if not self.admin_auth.can_manage_admins(user_id):
            await update.message.reply_text("❌ У вас нет прав для добавления администраторов.")
            context.user_data['waiting_for_admin_id'] = False
            return
        
        try:
            # Парсим ID пользователя
            admin_id_text = update.message.text.strip()
            admin_id = int(admin_id_text)
            
            # Проверяем, не является ли пользователь уже администратором
            if self.admin_auth.is_admin(admin_id):
                await update.message.reply_text("❌ Этот пользователь уже является администратором.")
                context.user_data['waiting_for_admin_id'] = False
                return
            
            # Получаем информацию о пользователе из базы или создаем запись
            user_info = self.db.get_user(admin_id)
            if not user_info:
                # Если пользователя нет в базе, создаем базовую запись
                self.db.add_user(admin_id)
                user_info = self.db.get_user(admin_id)
            
            # Добавляем администратора
            success = self.admin_auth.add_admin(
                user_id=admin_id,
                username=user_info[1] if user_info else None,
                first_name=user_info[2] if user_info else None,
                last_name=user_info[3] if user_info else None,
                role='admin',
                added_by=user_id
            )
            
            if success:
                username = f"@{user_info[1]}" if user_info and user_info[1] else f"ID:{admin_id}"
                await update.message.reply_text(f"✅ Пользователь {username} успешно добавлен как администратор.")
            else:
                await update.message.reply_text("❌ Не удалось добавить администратора.")
            
            context.user_data['waiting_for_admin_id'] = False
            
        except ValueError:
            await update.message.reply_text("❌ Неверный формат ID. Пожалуйста, отправьте числовой ID пользователя.")
        except Exception as e:
            await update.message.reply_text(f"❌ Ошибка добавления администратора: {str(e)}")
            context.user_data['waiting_for_admin_id'] = False
    
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
        application.add_handler(CallbackQueryHandler(self.consultation_callback, pattern="^consultation$"))
        
        # Message handlers
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_admin_id_message))
        
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
