import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Configuration
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')  # ID администратора для уведомлений

# Продамус Configuration
PRODAMUS_SHOP_ID = os.getenv('PRODAMUS_SHOP_ID')
PRODAMUS_SECRET_KEY = os.getenv('PRODAMUS_SECRET_KEY')
PRODAMUS_API_URL = os.getenv('PRODAMUS_API_URL', 'https://secure.payform.ru/init_payment')

# Канал Configuration
CHANNEL_ID = os.getenv('CHANNEL_ID')  # ID закрытого канала
CHANNEL_USERNAME = os.getenv('CHANNEL_USERNAME', '@women_club')  # Username канала

# Database
DATABASE_PATH = 'women_club.db'

# Subscription Settings
SUBSCRIPTION_PRICE = 1500  # Цена подписки в копейках (15 рублей)
SUBSCRIPTION_DURATION_DAYS = 30  # Длительность подписки в днях
REMINDER_DAYS_BEFORE = 3  # За сколько дней напоминать о продлении

# Messages
MESSAGES = {
    'welcome': 'Добро пожаловать в Женский клуб! 👋\n\nДля доступа к закрытому каналу необходимо оформить подписку на месяц.',
    'subscription_expired': 'Ваша подписка истекла! 😔\n\nДля возобновления доступа к закрытому каналу необходимо продлить подписку.',
    'subscription_ending': '⚠️ Внимание! Ваша подписка на Женский клуб истекает через {days} дней.\n\nПродлите подписку, чтобы не потерять доступ к закрытому каналу.',
    'payment_success': '✅ Оплата успешно принята!\n\nТеперь у вас есть доступ к закрытому каналу Женского клуба на 30 дней.',
    'access_denied': '❌ Доступ к каналу запрещен!\n\nВаша подписка истекла. Для получения доступа оформите подписку.',
    'admin_payment_notification': '💰 Новый платеж!\n\nПользователь: @{username} (ID: {user_id})\nСумма: {amount} руб.\nПодписка до: {expiry_date}',
    'admin_removal_notification': '🚫 Пользователь удален из канала\n\nПользователь: @{username} (ID: {user_id})\nПричина: неоплаченная подписка'
}
