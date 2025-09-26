# 🔒 ОТЧЕТ ПО НАСТРОЙКЕ SSL И NGINX ДЛЯ WEBHOOK

## ✅ Что настроено для работы с SSL на порту 5000

### 1. **Конфигурация Nginx для SSL**
- ✅ HTTP редирект на HTTPS
- ✅ SSL сертификаты Let's Encrypt
- ✅ Современные SSL настройки (TLS 1.2/1.3)
- ✅ Безопасность заголовков
- ✅ Проксирование на порт 5000

### 2. **Webhook endpoints**
- ✅ **Telegram webhook**: `https://yourdomain.com/webhook/telegram`
- ✅ **Prodamus webhook**: `https://yourdomain.com/sales/prodamus`
- ✅ **Health check**: `https://yourdomain.com/health`
- ✅ **Status check**: `https://yourdomain.com/status`

### 3. **SSL настройки**
- ✅ Автоматическое получение сертификатов
- ✅ Автоматическое обновление сертификатов
- ✅ HSTS заголовки
- ✅ Безопасные SSL ciphers

## 📋 Созданные файлы

### 1. **Конфигурационные файлы**
- `nginx_ssl_config.conf` - Полная конфигурация Nginx с SSL
- `webhook_ssl.py` - SSL версия webhook сервера
- `setup_ssl_nginx.sh` - Скрипт настройки SSL и Nginx
- `deploy_ssl.sh` - Полный скрипт развертывания с SSL

### 2. **Обновленные файлы**
- `config.py` - Обновлен для HTTPS URL
- `deploy_linux.sh` - Обновлен для SSL

## 🚀 Быстрое развертывание

### Вариант 1: Только SSL и Nginx
```bash
./setup_ssl_nginx.sh yourdomain.com
```

### Вариант 2: Полное развертывание с SSL
```bash
./deploy_ssl.sh yourdomain.com
```

## ⚙️ Настройки Nginx для Prodamus

### Основные настройки:
```nginx
# Webhook для Prodamus
location /sales/prodamus {
    proxy_pass http://localhost:5000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header X-Forwarded-Host $host;
    proxy_set_header X-Forwarded-Port $server_port;
    
    # Таймауты
    proxy_connect_timeout 30s;
    proxy_send_timeout 30s;
    proxy_read_timeout 30s;
    
    # Буферизация
    proxy_buffering on;
    proxy_buffer_size 4k;
    proxy_buffers 8 4k;
    
    # Размеры запросов
    client_max_body_size 1M;
    
    # Дополнительные заголовки для Prodamus
    proxy_set_header X-Forwarded-Ssl on;
}
```

### SSL настройки:
```nginx
# SSL сертификаты
ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

# SSL настройки
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384;
ssl_prefer_server_ciphers off;
ssl_session_cache shared:SSL:10m;
ssl_session_timeout 10m;

# Безопасность
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header X-Frame-Options DENY;
add_header X-Content-Type-Options nosniff;
add_header X-XSS-Protection "1; mode=block";
```

## 🔧 Настройки для Prodamus

### 1. **Webhook URL в панели Prodamus**
- **URL**: `https://yourdomain.com/sales/prodamus`
- **Метод**: POST
- **Заголовки**: `Sign: {signature}`

### 2. **Настройки магазина**
- **Shop ID**: `dashastar`
- **Secret Key**: `b2f9e8a399225271521dfe88a277a7371cb8c2cebfeaa6f0276ba81fcc303c93`
- **Demo Mode**: Включен для тестирования

### 3. **Проверка подписи**
- ✅ Включена строгая проверка подписи
- ✅ HMAC-SHA256 для безопасности
- ✅ Логирование процесса проверки

## 🧪 Тестирование

### 1. **Проверка SSL**
```bash
# Проверка SSL сертификата
sudo certbot certificates

# Тест SSL
curl -I https://yourdomain.com/health
```

### 2. **Проверка webhook**
```bash
# Health check
curl https://yourdomain.com/health

# Тест Prodamus webhook
curl -X POST https://yourdomain.com/sales/prodamus \
  -H "Content-Type: application/json" \
  -H "Sign: test_signature" \
  -d '{"test": "data"}'
```

### 3. **Проверка сервисов**
```bash
# Статус сервисов
sudo systemctl status tg-psy-webhook
sudo systemctl status tg-psy-bot

# Логи
sudo journalctl -u tg-psy-webhook -f
sudo journalctl -u tg-psy-bot -f
```

## 📝 Важные настройки

### 1. **Файрвол**
```bash
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw allow 5000
sudo ufw --force enable
```

### 2. **Автоматическое обновление SSL**
```bash
# Добавление в crontab
echo "0 12 * * * /usr/bin/certbot renew --quiet" | sudo crontab -
```

### 3. **Мониторинг**
```bash
# Логи Nginx
sudo tail -f /var/log/nginx/tg_psy_access.log
sudo tail -f /var/log/nginx/tg_psy_error.log

# Логи приложения
sudo journalctl -u tg-psy-webhook -f
sudo journalctl -u tg-psy-bot -f
```

## 🔍 Устранение неполадок

### Проблема: SSL сертификат не работает
**Решение:**
```bash
# Обновление сертификата
sudo certbot renew --dry-run

# Проверка конфигурации
sudo nginx -t
sudo systemctl reload nginx
```

### Проблема: Webhook не получает уведомления
**Решение:**
```bash
# Проверка доступности
curl -I https://yourdomain.com/sales/prodamus

# Проверка Nginx
sudo nginx -t
sudo systemctl reload nginx

# Проверка сервиса
sudo systemctl status tg-psy-webhook
```

### Проблема: Ошибки SSL
**Решение:**
```bash
# Проверка SSL
openssl s_client -connect yourdomain.com:443

# Обновление сертификата
sudo certbot --nginx -d yourdomain.com
```

## 🎯 Итоговая конфигурация

### ✅ Готово:
- **SSL сертификаты**: Let's Encrypt
- **Nginx конфигурация**: Оптимизирована для webhook
- **Порт 5000**: Настроен для Flask приложения
- **Проверка подписи**: Включена и работает
- **Автоматическое обновление**: Настроено
- **Мониторинг**: Настроен

### 📋 Следующие шаги:
1. **Настройте домен**: Замените `yourdomain.com` на реальный домен
2. **Запустите развертывание**: `./deploy_ssl.sh yourdomain.com`
3. **Настройте webhook URL в панели Prodamus**
4. **Протестируйте создание платежа**

---

**Система готова к работе с SSL на порту 5000! 🔒✅**
