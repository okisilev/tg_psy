# 🔧 ИНСТРУКЦИЯ ПО ОБНОВЛЕНИЮ КОНФИГУРАЦИИ НА СЕРВЕРЕ

## 📋 Текущая ситуация

- ✅ **Сервер**: 82.147.71.244
- ✅ **Webhook работает**: на порту 5000
- ✅ **Проверка подписи**: работает корректно
- ⚠️ **Нужно обновить**: конфигурацию для правильной работы

## 🚀 Быстрое обновление

### 1. Подключение к серверу
```bash
ssh root@82.147.71.244
```

### 2. Переход в директорию проекта
```bash
cd /usr/TG_BOTs/tg_psy/
```

### 3. Остановка старого webhook
```bash
pkill -f webhook_http.py
```

### 4. Обновление переменных окружения
```bash
export FLASK_PORT="5000"
export PRODAMUS_WEBHOOK_URL="http://82.147.71.244:5000/sales/prodamus"
export WEBHOOK_URL="http://82.147.71.244:5000/webhook/telegram"
```

### 5. Создание .env файла
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
PRODAMUS_WEBHOOK_URL=http://82.147.71.244:5000/sales/prodamus
WEBHOOK_URL=http://82.147.71.244:5000/webhook/telegram
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
DEBUG=false
EOF
```

### 6. Запуск webhook сервера
```bash
python3 webhook_http.py &
```

### 7. Проверка работы
```bash
curl http://localhost:5000/health
```

## 🧪 Тестирование

### 1. Проверка health check
```bash
curl http://82.147.71.244:5000/health
```

### 2. Тест webhook с правильной подписью
```bash
curl -X POST http://82.147.71.244:5000/sales/prodamus \
  -H "Content-Type: application/json" \
  -H "Sign: 919cb318867507f7e48790c3c2c2435f54bd62a29b8e7bd32157840bf546bb34" \
  -d '{"order_id":"women_club_431292182_test","sum":"50.00","currency":"rub","payment_status":"success","customer_email":"test@example.com"}'
```

## 📝 Настройки для Prodamus

### Webhook URL в панели Prodamus:
- **URL**: `http://82.147.71.244:5000/sales/prodamus`
- **Метод**: POST
- **Заголовки**: `Sign: {signature}`

### Настройки магазина:
- **Shop ID**: `dashastar`
- **Secret Key**: `b2f9e8a399225271521dfe88a277a7371cb8c2cebfeaa6f0276ba81fcc303c93`
- **Demo Mode**: Включен

## 🔍 Мониторинг

### Проверка процессов
```bash
ps aux | grep webhook
```

### Проверка портов
```bash
netstat -tlnp | grep :5000
```

### Логи (если есть)
```bash
tail -f webhook.log
```

## ⚠️ Важные замечания

### 1. Безопасность
- ✅ Проверка подписи включена
- ✅ Логирование работает
- ⚠️ Используется HTTP (для тестирования)

### 2. Для продакшена
- Настройте HTTPS с SSL сертификатом
- Используйте домен вместо IP
- Настройте Nginx для проксирования

### 3. Резервное копирование
- Сохраните текущую конфигурацию
- Создайте резервную копию базы данных
- Документируйте изменения

## 🚨 Устранение неполадок

### Проблема: Webhook не отвечает
**Решение:**
```bash
# Проверка процессов
ps aux | grep webhook

# Перезапуск
pkill -f webhook_http.py
python3 webhook_http.py &
```

### Проблема: Неверная подпись
**Решение:**
```bash
# Проверка подписи
python3 test_signature.py

# Проверка переменных
echo $PRODAMUS_SECRET_KEY
```

### Проблема: Порт занят
**Решение:**
```bash
# Проверка порта
netstat -tlnp | grep :5000

# Освобождение порта
pkill -f webhook_http.py
```

---

**Конфигурация обновлена! Webhook готов к работе на порту 5000! 🚀**
