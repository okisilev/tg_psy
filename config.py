import os

# Попытка загрузить переменные из .env файла
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️ python-dotenv не установлен. Используются переменные окружения системы.")

# Telegram Bot Configuration
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')  # ID главного администратора для уведомлений
ADMIN_IDS = os.getenv('ADMIN_IDS', '').split(',') if os.getenv('ADMIN_IDS') else []  # Список ID администраторов

# Webhook Configuration
WEBHOOK_URL = os.getenv('WEBHOOK_URL')  # https://yourdomain.com/webhook/telegram
WEBHOOK_PORT = int(os.getenv('WEBHOOK_PORT', '8443'))
WEBHOOK_LISTEN = os.getenv('WEBHOOK_LISTEN', '0.0.0.0')
WEBHOOK_SSL_CERT = os.getenv('WEBHOOK_SSL_CERT', './ssl/cert.pem')
WEBHOOK_SSL_PRIV = os.getenv('WEBHOOK_SSL_PRIV', './ssl/private.key')

# Server Configuration
FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
FLASK_PORT = int(os.getenv('FLASK_PORT', '5000'))
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Продамус Configuration
PRODAMUS_SHOP_ID = os.getenv('PRODAMUS_SHOP_ID', 'dashastar')  # Shop ID из URL dashastar.payform.ru
PRODAMUS_SECRET_KEY = os.getenv('PRODAMUS_SECRET_KEY', 'b2f9e8a399225271521dfe88a277a7371cb8c2cebfeaa6f0276ba81fcc303c93')
PRODAMUS_API_URL = os.getenv('PRODAMUS_API_URL', 'https://dashastar.payform.ru/init_payment')
PRODAMUS_DEMO_MODE = os.getenv('PRODAMUS_DEMO_MODE', 'true').lower() == 'true'  # Включаем демо-режим по умолчанию

# Канал Configuration
CHANNEL_ID = os.getenv('CHANNEL_ID', '-1001234567890')  # ID закрытого канала (замените на реальный ID)
CHANNEL_USERNAME = os.getenv('CHANNEL_USERNAME', '@women_club')  # Username канала
CHANNEL_INVITE_LINK = os.getenv('CHANNEL_INVITE_LINK', 'https://t.me/+gstVWYW2Kgo2OGYy')  # Ссылка-приглашение в канал

# WhatsApp Configuration
WHATSAPP_NUMBER = os.getenv('WHATSAPP_NUMBER', '+79149425115')  # Номер WhatsApp для консультаций

# Database
DATABASE_PATH = 'women_club.db'

# Subscription Settings
SUBSCRIPTION_PRICE = 1500  # Цена подписки в копейках (15 рублей)
SUBSCRIPTION_DURATION_DAYS = 30  # Длительность подписки в днях
REMINDER_DAYS_BEFORE = 3  # За сколько дней напоминать о продлении

# Messages
MESSAGES = {
    'welcome': 'Добро пожаловать в Женский клуб «СОСТОЯНИЕ»! 👋\n\nДля доступа к закрытому каналу необходимо оформить подписку на месяц.',
    'subscription_expired': 'Ваша подписка истекла! 😔\n\nДля возобновления доступа к закрытому каналу необходимо продлить подписку.',
    'subscription_ending': '⚠️ Внимание! Ваша подписка на Женский клуб «СОСТОЯНИЕ» истекает через {days} дней.\n\nПродлите подписку, чтобы не потерять доступ к закрытому каналу.',
    'payment_success': '✅ Оплата успешно принята!\n\nТеперь у вас есть доступ к закрытому каналу Женского клуба «СОСТОЯНИЕ» на 30 дней.',
    'access_denied': '❌ Доступ к каналу запрещен!\n\nВаша подписка истекла. Для получения доступа оформите подписку.',
    'consultation_info': '💬 Индивидуальная консультация\n\nДля записи на индивидуальную консультацию перейдите в WhatsApp по номеру {whatsapp_number}\n\nКонсультации проводятся:\n• Онлайн\n• В удобное для вас время\n• Индивидуальный подход',
    'admin_payment_notification': '💰 Новый платеж!\n\nПользователь: @{username} (ID: {user_id})\nСумма: {amount} руб.\nПодписка до: {expiry_date}',
    'admin_removal_notification': '🚫 Пользователь удален из канала\n\nПользователь: @{username} (ID: {user_id})\nПричина: неоплаченная подписка'
}
