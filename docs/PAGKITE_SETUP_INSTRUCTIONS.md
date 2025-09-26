# 🌐 НАСТРОЙКА PAGKITE ДЛЯ WEBHOOK

## 📋 Обзор

PageKite позволяет создать публичный HTTPS URL для локального webhook сервера, что необходимо для работы с Prodamus и Telegram.

## 🚀 Быстрая настройка

### 1. Установка PageKite

```bash
pip install pagekite
```

### 2. Запуск сервисов

```bash
# Запуск webhook сервера и PageKite
./start_pagekite_webhook.sh
```

### 3. Проверка работы

```bash
# Тест PageKite webhook
python3 test_pagekite_webhook.py
```

## 🔧 Подробная настройка

### 1. Установка PageKite

```bash
# Установка через pip
pip install pagekite

# Проверка установки
pagekite.py --help
```

### 2. Настройка переменных окружения

```bash
# Установка переменных
export FLASK_PORT="5000"
export PRODAMUS_WEBHOOK_URL="https://dashastar.pagekite.me/sales/prodamus"
export WEBHOOK_URL="https://dashastar.pagekite.me/webhook/telegram"
```

### 3. Создание .env файла

```bash
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
PRODAMUS_WEBHOOK_URL=https://dashastar.pagekite.me/sales/prodamus
WEBHOOK_URL=https://dashastar.pagekite.me/webhook/telegram
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
DEBUG=false
EOF
```

### 4. Запуск webhook сервера

```bash
# Запуск в фоне
python3 webhook_http.py &
```

### 5. Запуск PageKite

```bash
# Запуск PageKite туннеля
pagekite.py 5000 dashastar.pagekite.me &
```

## 🧪 Тестирование

### 1. Проверка health endpoint

```bash
curl https://dashastar.pagekite.me/health
```

### 2. Тест Prodamus webhook

```bash
curl -X POST https://dashastar.pagekite.me/sales/prodamus \
  -H "Content-Type: application/json" \
  -H "Sign: 30ba444dc24a268bdb78669632c6e0777652c0e63217b6cbc9adcb5fb2a0adaa" \
  -d '{"order_id":"women_club_431292182_test","sum":"50.00","currency":"rub","payment_status":"success"}'
```

### 3. Тест Telegram webhook

```bash
curl -X POST https://dashastar.pagekite.me/webhook/telegram \
  -H "Content-Type: application/json" \
  -d '{"update_id":123456789,"message":{"message_id":1,"from":{"id":431292182},"chat":{"id":431292182},"date":1234567890,"text":"/start"}}'
```

## 📝 Настройки для внешних сервисов

### Prodamus

- **Webhook URL**: `https://dashastar.pagekite.me/sales/prodamus`
- **Метод**: POST
- **Заголовки**: `Sign: {signature}`
- **Content-Type**: `application/json`

### Telegram

- **Webhook URL**: `https://dashastar.pagekite.me/webhook/telegram`
- **Метод**: POST
- **Content-Type**: `application/json`

## 🔧 Управление сервисами

### Запуск

```bash
# Запуск всех сервисов
./start_pagekite_webhook.sh
```

### Остановка

```bash
# Остановка всех сервисов
./stop_pagekite_webhook.sh
```

### Проверка статуса

```bash
# Проверка процессов
ps aux | grep -E "(webhook_http.py|pagekite.py)"

# Проверка портов
netstat -tlnp | grep :5000
```

## ⚠️ Важные замечания

### 1. Безопасность

- PageKite создает публичный URL
- Убедитесь, что webhook сервер защищен
- Используйте проверку подписи для Prodamus

### 2. Стабильность

- PageKite может быть нестабильным
- Рекомендуется мониторинг соединения
- Настройте автоперезапуск при сбоях

### 3. Альтернативы

- Используйте VPS с публичным IP
- Настройте SSL сертификат
- Используйте облачные сервисы

## 🚨 Устранение неполадок

### Проблема: PageKite не подключается

**Решение:**
```bash
# Проверка интернет соединения
ping pagekite.net

# Перезапуск PageKite
pkill -f pagekite.py
pagekite.py 5000 dashastar.pagekite.me &
```

### Проблема: Webhook не отвечает

**Решение:**
```bash
# Проверка webhook сервера
curl http://localhost:5000/health

# Перезапуск webhook
pkill -f webhook_http.py
python3 webhook_http.py &
```

### Проблема: SSL ошибки

**Решение:**
```bash
# Проверка SSL
curl -k https://dashastar.pagekite.me/health

# Обновление PageKite
pip install --upgrade pagekite
```

## 📊 Мониторинг

### Логи

```bash
# Логи webhook сервера
tail -f webhook.log

# Логи PageKite
tail -f pagekite.log
```

### Статистика

```bash
# Статистика соединений
netstat -an | grep :5000

# Использование памяти
ps aux | grep -E "(webhook_http.py|pagekite.py)"
```

---

**PageKite настроен! Webhook доступен по адресу: https://dashastar.pagekite.me 🎉**
