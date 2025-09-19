# 🔗 Настройка Webhook и переменных окружения

## 📋 Переменные окружения для настройки

### 1. Telegram Bot Configuration
```bash
# Токен бота (обязательно)
export BOT_TOKEN="8455794146:AAFf9DEcTxLnJfG-HWWmzwpSjTRDzNE3px8"

# ID администраторов (обязательно)
export ADMIN_CHAT_ID="431292182,190545165"
export ADMIN_IDS="431292182,190545165"

# ID канала (обязательно для добавления пользователей)
export CHANNEL_ID="-1001234567890"  # Замените на реальный ID канала
export CHANNEL_USERNAME="@your_channel_username"  # Замените на реальный username
export CHANNEL_INVITE_LINK="https://t.me/+gstVWYW2Kgo2OGYy"  # Замените на реальную ссылку
```

### 2. Prodamus Configuration
```bash
# Настройки Prodamus (уже настроены)
export PRODAMUS_SHOP_ID="dashastar"
export PRODAMUS_SECRET_KEY="b2f9e8a399225271521dfe88a277a7371cb8c2cebfeaa6f0276ba81fcc303c93"
export PRODAMUS_DEMO_MODE="true"
```

### 3. Webhook URLs (ВАЖНО!)
```bash
# URL для Telegram webhook
export WEBHOOK_URL="https://--help/webhook/telegram"

# URL для Prodamus webhook
export PRODAMUS_WEBHOOK_URL="https://--help/webhook/prodamus"
```

### 4. Server Configuration
```bash
# Настройки сервера
export FLASK_HOST="0.0.0.0"
export FLASK_PORT="5000"
export DEBUG="false"
```

## 🌐 Настройка домена и SSL

### 1. Получение домена
- Зарегистрируйте домен (например, `--help`)
- Настройте DNS записи для вашего сервера

### 2. Настройка SSL сертификата
```bash
# Установка Let's Encrypt (рекомендуется)
sudo apt install certbot
sudo certbot certonly --standalone -d --help

# Или используйте самоподписанный сертификат для тестирования
openssl req -x509 -newkey rsa:4096 -keyout ssl/private.key -out ssl/cert.pem -days 365 -nodes
```

### 3. Настройка Nginx (рекомендуется)
```nginx
server {
    listen 443 ssl;
    server_name --help;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/private.key;
    
    location /webhook/telegram {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /webhook/prodamus {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🚀 Запуск системы

### 1. Установка переменных окружения
```bash
# Создайте файл .env
cat > .env << 'EOF'
# Telegram Bot Configuration
BOT_TOKEN=8455794146:AAFf9DEcTxLnJfG-HWWmzwpSjTRDzNE3px8
ADMIN_CHAT_ID=431292182,190545165
ADMIN_IDS=431292182,190545165
CHANNEL_ID=-1001234567890
CHANNEL_USERNAME=@your_channel_username
CHANNEL_INVITE_LINK=https://t.me/+gstVWYW2Kgo2OGYy

# Prodamus Configuration
PRODAMUS_SHOP_ID=dashastar
PRODAMUS_SECRET_KEY=b2f9e8a399225271521dfe88a277a7371cb8c2cebfeaa6f0276ba81fcc303c93
PRODAMUS_DEMO_MODE=true
PRODAMUS_WEBHOOK_URL=https://--help/webhook/prodamus

# Webhook Configuration
WEBHOOK_URL=https://--help/webhook/telegram
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
DEBUG=false
EOF
```

### 2. Запуск webhook сервера
```bash
# Запуск сервера
python3 start_webhook.py
```

### 3. Настройка в панели Prodamus
1. Войдите в панель управления Prodamus
2. Перейдите в раздел "Настройки"
3. Установите webhook URL: `https://--help/webhook/prodamus`
4. Включите демо-режим для тестирования

## 🧪 Тестирование

### 1. Проверка webhook
```bash
# Проверка health check
curl https://--help/health

# Тест webhook Prodamus
curl -X POST https://--help/webhook/prodamus \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'
```

### 2. Создание тестового платежа
```bash
# Запуск теста
python3 test_full_payment_flow.py
```

## 📝 Важные замечания

### 1. Безопасность
- ✅ Используйте HTTPS для всех webhook URL
- ✅ Проверяйте подписи от Prodamus
- ✅ Ограничьте доступ к серверу

### 2. Мониторинг
- ✅ Проверяйте логи webhook сервера
- ✅ Мониторьте статус платежей
- ✅ Отслеживайте добавление пользователей в канал

### 3. Резервное копирование
- ✅ Регулярно создавайте резервные копии базы данных
- ✅ Сохраняйте конфигурационные файлы
- ✅ Документируйте изменения

## 🔧 Устранение неполадок

### Проблема: Webhook не получает уведомления
**Решение:**
1. Проверьте, что сервер доступен извне
2. Убедитесь, что URL правильный в панели Prodamus
3. Проверьте логи сервера

### Проблема: Пользователи не добавляются в канал
**Решение:**
1. Проверьте CHANNEL_ID в конфигурации
2. Убедитесь, что бот является администратором канала
3. Проверьте права бота в канале

### Проблема: Ошибки SSL
**Решение:**
1. Проверьте сертификат SSL
2. Убедитесь, что домен правильно настроен
3. Используйте Let's Encrypt для автоматического обновления

---

**Система готова к настройке и тестированию! 🚀**
