import asyncio
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler
from telegram.constants import ParseMode
from database import Database
from config import ADMIN_CHAT_ID

class AdminPanel:
    def __init__(self, bot_instance):
        self.bot = bot_instance
        self.db = Database()
    
    async def admin_report_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик отчета по платежам"""
        query = update.callback_query
        await query.answer()
        
        keyboard = [
            [InlineKeyboardButton("📅 За последние 7 дней", callback_data="report_7days")],
            [InlineKeyboardButton("📅 За последние 30 дней", callback_data="report_30days")],
            [InlineKeyboardButton("📅 За последние 90 дней", callback_data="report_90days")],
            [InlineKeyboardButton("📅 Выбрать период", callback_data="report_custom")],
            [InlineKeyboardButton("🔙 Назад", callback_data="admin_back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "📊 Отчет по платежам\n\nВыберите период:",
            reply_markup=reply_markup
        )
    
    async def generate_report(self, update: Update, context: ContextTypes.DEFAULT_TYPE, days: int = None, start_date: str = None, end_date: str = None):
        """Генерация отчета по платежам"""
        query = update.callback_query
        await query.answer()
        
        try:
            # Определяем период
            if days:
                end_date = datetime.now()
                start_date = end_date - timedelta(days=days)
            else:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
            
            start_str = start_date.strftime('%Y-%m-%d')
            end_str = end_date.strftime('%Y-%m-%d')
            
            # Получаем данные из базы
            payments = self.db.get_payments_report(start_str, end_str)
            total_amount = self.db.get_total_payments_amount(start_str, end_str)
            
            # Формируем отчет
            report = f"📊 Отчет по платежам\n"
            report += f"📅 Период: {start_str} - {end_str}\n\n"
            report += f"💰 Общая сумма: {total_amount / 100:.2f} руб.\n"
            report += f"📈 Количество платежей: {len(payments)}\n\n"
            
            if payments:
                report += "📋 Детализация:\n"
                for payment in payments[:10]:  # Показываем последние 10
                    user_info = f"@{payment[7]}" if payment[7] else f"ID:{payment[1]}"
                    amount = payment[3] / 100
                    date = payment[6][:10]
                    report += f"• {user_info}: {amount:.2f} руб. ({date})\n"
                
                if len(payments) > 10:
                    report += f"\n... и еще {len(payments) - 10} платежей"
            else:
                report += "📭 Платежей за указанный период не найдено"
            
            keyboard = [
                [InlineKeyboardButton("📊 Новый отчет", callback_data="admin_report")],
                [InlineKeyboardButton("🔙 Главное меню", callback_data="admin_back")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(report, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
            
        except Exception as e:
            await query.edit_message_text(f"❌ Ошибка генерации отчета: {str(e)}")
    
    async def admin_users_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик управления пользователями"""
        query = update.callback_query
        await query.answer()
        
        # Получаем статистику пользователей
        active_subscriptions = len(self.db.get_expiring_subscriptions(365))  # Все активные
        total_users = len(self.db.get_all_users())
        
        keyboard = [
            [InlineKeyboardButton("👥 Все пользователи", callback_data="users_all")],
            [InlineKeyboardButton("✅ С активной подпиской", callback_data="users_active")],
            [InlineKeyboardButton("❌ С истекшей подпиской", callback_data="users_expired")],
            [InlineKeyboardButton("🔙 Назад", callback_data="admin_back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            f"👥 Управление пользователями\n\n"
            f"📊 Статистика:\n"
            f"• Всего пользователей: {total_users}\n"
            f"• С активной подпиской: {active_subscriptions}\n"
            f"• С истекшей подпиской: {total_users - active_subscriptions}",
            reply_markup=reply_markup
        )
    
    async def admin_check_subscriptions_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Проверка подписок"""
        query = update.callback_query
        await query.answer()
        
        # Получаем подписки, которые скоро истекут
        expiring = self.db.get_expiring_subscriptions(3)
        expired = self.db.get_expired_subscriptions()
        
        message = f"🔄 Проверка подписок\n\n"
        message += f"⚠️ Истекают в ближайшие 3 дня: {len(expiring)}\n"
        message += f"❌ Уже истекли: {len(expired)}\n\n"
        
        if expiring:
            message += "📋 Истекающие подписки:\n"
            for sub in expiring[:5]:
                username = sub[7] if sub[7] else f"ID:{sub[1]}"
                end_date = sub[5][:10]
                message += f"• @{username} до {end_date}\n"
        
        if expired:
            message += "\n📋 Истекшие подписки:\n"
            for sub in expired[:5]:
                username = sub[7] if sub[7] else f"ID:{sub[1]}"
                end_date = sub[5][:10]
                message += f"• @{username} с {end_date}\n"
        
        keyboard = [
            [InlineKeyboardButton("🔄 Обновить", callback_data="admin_check_subscriptions")],
            [InlineKeyboardButton("🔙 Назад", callback_data="admin_back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(message, reply_markup=reply_markup)
    
    async def admin_back_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Возврат в главное меню админки"""
        query = update.callback_query
        await query.answer()
        
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
    
    def setup_admin_handlers(self, application):
        """Настройка обработчиков админ-панели"""
        # Отчеты
        application.add_handler(CallbackQueryHandler(self.admin_report_callback, pattern="^admin_report$"))
        application.add_handler(CallbackQueryHandler(lambda u, c: self.generate_report(u, c, 7), pattern="^report_7days$"))
        application.add_handler(CallbackQueryHandler(lambda u, c: self.generate_report(u, c, 30), pattern="^report_30days$"))
        application.add_handler(CallbackQueryHandler(lambda u, c: self.generate_report(u, c, 90), pattern="^report_90days$"))
        
        # Пользователи
        application.add_handler(CallbackQueryHandler(self.admin_users_callback, pattern="^admin_users$"))
        application.add_handler(CallbackQueryHandler(self.admin_check_subscriptions_callback, pattern="^admin_check_subscriptions$"))
        
        # Навигация
        application.add_handler(CallbackQueryHandler(self.admin_back_callback, pattern="^admin_back$"))
