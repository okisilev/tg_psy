# 🔧 Настройка переменных окружения

## 📋 Обязательные переменные для работы системы

### 1. Telegram Bot Configuration
```bash
export BOT_TOKEN="8455794146:AAFf9DEcTxLnJfG-HWWmzwpSjTRDzNE3px8"
export ADMIN_CHAT_ID="431292182,190545165"
export ADMIN_IDS="431292182,190545165"
export CHANNEL_ID="-1001234567890"  # ⚠️ ЗАМЕНИТЕ НА РЕАЛЬНЫЙ ID КАНАЛА
export CHANNEL_USERNAME="@your_channel_username"  # ⚠️ ЗАМЕНИТЕ НА РЕАЛЬНЫЙ USERNAME
export CHANNEL_INVITE_LINK="https://t.me/+gstVWYW2Kgo2OGYy"  # ⚠️ ЗАМЕНИТЕ НА РЕАЛЬНУЮ ССЫЛКУ
```

### 2. Prodamus Configuration
```bash
export PRODAMUS_SHOP_ID="dashastar"
export PRODAMUS_SECRET_KEY="b2f9e8a399225271521dfe88a277a7371cb8c2cebfeaa6f0276ba81fcc303c93"
export PRODAMUS_DEMO_MODE="true"
export PRODAMUS_WEBHOOK_URL="https://--help/webhook/prodamus"  # ⚠️ ЗАМЕНИТЕ НА РЕАЛЬНЫЙ ДОМЕН
```

### 3. Webhook Configuration
```bash
export WEBHOOK_URL="https://--help/webhook/telegram"  # ⚠️ ЗАМЕНИТЕ НА РЕАЛЬНЫЙ ДОМЕН
export FLASK_HOST="0.0.0.0"
export FLASK_PORT="5000"
export DEBUG="false"
```

## 🚀 Быстрая настройка

### Вариант 1: Экспорт переменных в терминале
```bash
# Скопируйте и выполните все команды выше в терминале
export BOT_TOKEN="8455794146:AAFf9DEcTxLnJfG-HWWmzwpSjTRDzNE3px8"
export ADMIN_CHAT_ID="431292182,190545165"
# ... и так далее
```

### Вариант 2: Создание .env файла
```bash
# Создайте файл .env
cat > .env << 'EOF'
BOT_TOKEN=8455794146:AAFf9DEcTxLnJfG-HWWmzwpSjTRDzNE3px8
ADMIN_CHAT_ID=431292182,190545165
ADMIN_IDS=431292182,190545165
CHANNEL_ID=-1001234567890
CHANNEL_USERNAME=@your_channel_username
CHANNEL_INVITE_LINK=https://t.me/+gstVWYW2Kgo2OGYy
PRODAMUS_SHOP_ID=dashastar
PRODAMUS_SECRET_KEY=b2f9e8a399225271521dfe88a277a7371cb8c2cebfeaa6f0276ba81fcc303c93
PRODAMUS_DEMO_MODE=true
PRODAMUS_WEBHOOK_URL=https://--help/webhook/prodamus
WEBHOOK_URL=https://--help/webhook/telegram
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
DEBUG=false
EOF

# Загрузите переменные
source .env
```

## 🔍 Проверка конфигурации

```bash
# Запустите проверку
python3 check_config.py
```

## ⚠️ Важные замечания

### 1. Замените тестовые значения на реальные:
- `CHANNEL_ID` - реальный ID вашего канала
- `CHANNEL_USERNAME` - реальный username канала
- `CHANNEL_INVITE_LINK` - реальная ссылка-приглашение
- `--help` - ваш реальный домен

### 2. Настройка канала:
1. Создайте приватный канал в Telegram
2. Добавьте бота как администратора канала
3. Получите ID канала (начинается с -100)
4. Получите username канала (начинается с @)
5. Создайте ссылку-приглашение

### 3. Настройка домена:
1. Зарегистрируйте домен
2. Настройте DNS записи
3. Установите SSL сертификат
4. Настройте Nginx или другой веб-сервер

## 🧪 Тестирование

```bash
# 1. Проверка конфигурации
python3 check_config.py

# 2. Тест создания платежа
python3 test_payment_creation.py

# 3. Запуск webhook сервера
python3 start_webhook.py

# 4. Полный тест системы
python3 test_full_payment_flow.py
```

## 📝 Следующие шаги

1. **Настройте реальный канал** - замените тестовые значения
2. **Настройте домен** - замените --help на реальный домен
3. **Запустите webhook сервер** - `python3 start_webhook.py`
4. **Протестируйте платеж** - откройте URL платежа в браузере
5. **Проверьте webhook** - убедитесь, что уведомления приходят

---

**Система готова к настройке! 🚀**
