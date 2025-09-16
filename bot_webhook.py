import logging
import asyncio
from flask import Flask, request, jsonify
from telegram import Update, Bot
from telegram.ext import Application, ContextTypes
from telegram.error import TelegramError
from telegram.constants import ParseMode
import threading
import queue
import json
from datetime import datetime

from config import (
    BOT_TOKEN, ADMIN_CHAT_ID, CHANNEL_ID, CHANNEL_USERNAME,
    MESSAGES, SUBSCRIPTION_PRICE, WEBHOOK_URL, DEBUG
)
from database import Database
from prodamus import ProdаmusAPI
from scheduler import SubscriptionScheduler
from admin_panel import AdminPanel
from channel_manager import ChannelManager

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO if not DEBUG else logging.DEBUG
)
logger = logging.getLogger(__name__)

# Flask приложение
app = Flask(__name__)

# Инициализация компонентов
db = Database()
prodamus = ProdаmusAPI()
channel_manager = ChannelManager()

# Глобальные переменные для бота
bot_instance = None
application = None
scheduler = None
admin_panel = None

# Очередь для обработки обновлений
update_queue = queue.Queue()

class WebhookBot:
    def __init__(self):
        global bot_instance, application, scheduler, admin_panel
        self.db = db
        self.prodamus = prodamus
        self.channel_manager = channel_manager
        
        # Инициализация бота
        self.bot = Bot(token=BOT_TOKEN)
        
        # Инициализация application для обработки обновлений
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Инициализация компонентов
        scheduler = SubscriptionScheduler(self)
        admin_panel = AdminPanel(self)
        
        # Настройка обработчиков
        self.setup_handlers()
        
        bot_instance = self
        
        logger.info("WebhookBot инициализирован")

    def setup_handlers(self):
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
        admin_panel.setup_admin_handlers(application)

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

    async def send_message_to_user(self, user_id: int, text: str, reply_markup=None):
        """Отправка сообщения пользователю"""
        try:
            await self.bot.send_message(
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
            
            await self.bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                text=message
            )
            logger.info(f"✅ Уведомление администратору отправлено")
            
        except Exception as e:
            logger.error(f"❌ Ошибка уведомления администратора: {e}")

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
        await admin_panel.admin_report_callback(update, context)

    async def start_scheduler(self):
        """Запуск планировщика задач"""
        await scheduler.start()

    def setup_webhook(self):
        """Настройка webhook"""
        try:
            # Удаляем старый webhook
            asyncio.run(self.bot.delete_webhook())
            
            # Устанавливаем новый webhook
            asyncio.run(self.bot.set_webhook(
                url=WEBHOOK_URL,
                allowed_updates=["message", "callback_query"]
            ))
            
            logger.info(f"Webhook установлен: {WEBHOOK_URL}")
            
        except Exception as e:
            logger.error(f"Ошибка настройки webhook: {e}")

# Глобальная переменная для бота
webhook_bot = None

def process_updates():
    """Обработка обновлений в отдельном потоке"""
    while True:
        try:
            # Получаем обновление из очереди
            update_data = update_queue.get(timeout=1)
            
            # Создаем объект Update
            update = Update.de_json(update_data, webhook_bot.bot)
            
            # Обрабатываем обновление
            asyncio.run(application.process_update(update))
            
            update_queue.task_done()
            
        except queue.Empty:
            continue
        except Exception as e:
            logger.error(f"Ошибка обработки обновления: {e}")

# Flask маршруты
@app.route('/webhook/telegram', methods=['POST'])
def telegram_webhook():
    """Обработчик webhook от Telegram"""
    try:
        # Получаем данные от Telegram
        update_data = request.get_json()
        
        if not update_data:
            logger.error("Пустые данные от Telegram webhook")
            return jsonify({'status': 'error', 'message': 'Empty data'}), 400
        
        # Добавляем обновление в очередь для обработки
        update_queue.put(update_data)
        
        logger.debug(f"Получено обновление: {update_data.get('update_id')}")
        
        return jsonify({'status': 'success'})
        
    except Exception as e:
        logger.error(f"Ошибка обработки Telegram webhook: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/webhook/prodamus', methods=['POST'])
def prodamus_webhook():
    """Обработчик webhook от Продамус"""
    try:
        # Получаем данные от Продамус
        data = request.get_json()
        
        if not data:
            logger.error("Пустые данные от webhook")
            return jsonify({'status': 'error', 'message': 'Empty data'}), 400
        
        # Получаем подпись из заголовков
        signature = request.headers.get('X-Signature')
        
        if not signature:
            logger.error("Отсутствует подпись в webhook")
            return jsonify({'status': 'error', 'message': 'Missing signature'}), 400
        
        # Проверяем подпись
        if not prodamus.verify_webhook(data, signature):
            logger.error("Неверная подпись webhook")
            return jsonify({'status': 'error', 'message': 'Invalid signature'}), 400
        
        # Обрабатываем платеж
        order_id = data.get('order_id')
        status = data.get('status')
        amount = data.get('amount')
        
        logger.info(f"Webhook получен: order_id={order_id}, status={status}, amount={amount}")
        
        if status == 'success':
            # Платеж успешен
            handle_successful_payment(order_id, amount, data)
        elif status == 'failed':
            # Платеж не прошел
            handle_failed_payment(order_id, data)
        
        return jsonify({'status': 'success'})
        
    except Exception as e:
        logger.error(f"Ошибка обработки webhook: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

def handle_successful_payment(order_id: str, amount: int, webhook_data: dict):
    """Обработка успешного платежа"""
    try:
        # Извлекаем user_id из custom_fields
        custom_fields = webhook_data.get('custom_fields', {})
        user_id = int(custom_fields.get('user_id'))
        
        # Обновляем статус платежа в базе данных
        db.add_payment(user_id, order_id, amount, 'success')
        
        # Создаем подписку
        db.create_subscription(user_id, order_id, amount)
        
        # Получаем информацию о пользователе
        user = db.get_user(user_id)
        subscription = db.get_active_subscription(user_id)
        
        logger.info(f"Подписка активирована для пользователя {user_id}")
        
        # Активируем подписку через бота
        if webhook_bot:
            asyncio.run(webhook_bot.activate_subscription(user_id, order_id, amount))
        
    except Exception as e:
        logger.error(f"Ошибка обработки успешного платежа: {e}")

def handle_failed_payment(order_id: str, webhook_data: dict):
    """Обработка неудачного платежа"""
    try:
        # Извлекаем user_id из custom_fields
        custom_fields = webhook_data.get('custom_fields', {})
        user_id = int(custom_fields.get('user_id'))
        
        # Обновляем статус платежа в базе данных
        amount = webhook_data.get('amount', 0)
        db.add_payment(user_id, order_id, amount, 'failed')
        
        logger.info(f"Платеж не прошел для пользователя {user_id}")
        
    except Exception as e:
        logger.error(f"Ошибка обработки неудачного платежа: {e}")

@app.route('/health', methods=['GET'])
def health_check():
    """Проверка здоровья сервиса"""
    return jsonify({
        'status': 'healthy', 
        'timestamp': datetime.now().isoformat(),
        'bot_status': 'running' if webhook_bot else 'stopped'
    })

@app.route('/status', methods=['GET'])
def status():
    """Статус сервиса"""
    try:
        # Получаем статистику из базы данных
        total_users = len(db.get_all_users())
        active_subscriptions = len(db.get_users_with_active_subscriptions())
        
        return jsonify({
            'status': 'running',
            'bot_status': 'running' if webhook_bot else 'stopped',
            'total_users': total_users,
            'active_subscriptions': active_subscriptions,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

def init_bot():
    """Инициализация бота"""
    global webhook_bot
    
    try:
        # Создаем экземпляр бота
        webhook_bot = WebhookBot()
        
        # Настраиваем webhook
        webhook_bot.setup_webhook()
        
        # Запускаем планировщик в отдельном потоке
        def run_scheduler():
            asyncio.run(webhook_bot.start_scheduler())
        
        scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        scheduler_thread.start()
        
        # Запускаем обработку обновлений в отдельном потоке
        update_thread = threading.Thread(target=process_updates, daemon=True)
        update_thread.start()
        
        logger.info("Бот успешно инициализирован")
        
    except Exception as e:
        logger.error(f"Ошибка инициализации бота: {e}")

if __name__ == '__main__':
    # Инициализируем бота
    init_bot()
    
    # Запускаем Flask приложение
    from config import FLASK_HOST, FLASK_PORT, DEBUG
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=DEBUG)
