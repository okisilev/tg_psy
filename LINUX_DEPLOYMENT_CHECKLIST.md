# 🐧 ЧЕК-ЛИСТ РАЗВЕРТЫВАНИЯ НА LINUX СЕРВЕРЕ

## 📋 Предварительные требования

### 1. Системные требования
- ✅ **OS**: Ubuntu 20.04+ / CentOS 7+ / Debian 10+
- ✅ **Python**: 3.8+ (рекомендуется 3.10+)
- ✅ **RAM**: минимум 1GB (рекомендуется 2GB+)
- ✅ **Диск**: минимум 10GB свободного места
- ✅ **Сеть**: открытые порты 80, 443, 5000

### 2. Установка зависимостей
```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Python и pip
sudo apt install python3 python3-pip python3-venv -y

# Установка дополнительных пакетов
sudo apt install curl wget git nginx certbot -y
```

## 🔧 Настройка проекта

### 1. Клонирование и настройка
```bash
# Клонирование проекта
git clone <repository_url> /opt/tg_psy
cd /opt/tg_psy

# Создание виртуального окружения
python3 -m venv venv
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt
```

### 2. Настройка переменных окружения
```bash
# Создание .env файла
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
PRODAMUS_WEBHOOK_URL=http://YOUR_DOMAIN.com:5000/sales/prodamus

# Webhook Configuration
WEBHOOK_URL=http://YOUR_DOMAIN.com:5000/webhook/telegram
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
DEBUG=false
EOF
```

### 3. Настройка базы данных
```bash
# Инициализация базы данных
python3 -c "from database import Database; db = Database(); print('База данных инициализирована')"
```

## 🌐 Настройка веб-сервера (Nginx)

### 1. Конфигурация Nginx
```bash
# Создание конфигурации
sudo tee /etc/nginx/sites-available/tg_psy << 'EOF'
server {
    listen 80;
    server_name YOUR_DOMAIN.com;
    
    location /webhook/telegram {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /sales/prodamus {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /health {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
EOF

# Активация конфигурации
sudo ln -s /etc/nginx/sites-available/tg_psy /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 2. Настройка SSL (Let's Encrypt)
```bash
# Получение SSL сертификата
sudo certbot --nginx -d YOUR_DOMAIN.com

# Автоматическое обновление
sudo crontab -e
# Добавить строку:
# 0 12 * * * /usr/bin/certbot renew --quiet
```

## 🚀 Настройка systemd сервисов

### 1. Webhook сервис
```bash
# Создание сервиса webhook
sudo tee /etc/systemd/system/tg-psy-webhook.service << 'EOF'
[Unit]
Description=TG Psy Webhook Server
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/tg_psy
Environment=PATH=/opt/tg_psy/venv/bin
ExecStart=/opt/tg_psy/venv/bin/python webhook_http.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Активация сервиса
sudo systemctl daemon-reload
sudo systemctl enable tg-psy-webhook
sudo systemctl start tg-psy-webhook
```

### 2. Telegram Bot сервис
```bash
# Создание сервиса бота
sudo tee /etc/systemd/system/tg-psy-bot.service << 'EOF'
[Unit]
Description=TG Psy Telegram Bot
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/tg_psy
Environment=PATH=/opt/tg_psy/venv/bin
ExecStart=/opt/tg_psy/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Активация сервиса
sudo systemctl daemon-reload
sudo systemctl enable tg-psy-bot
sudo systemctl start tg-psy-bot
```

## 🔥 Настройка файрвола

### 1. UFW (Ubuntu)
```bash
# Настройка файрвола
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw allow 5000
sudo ufw --force enable
```

### 2. iptables (CentOS/RHEL)
```bash
# Настройка iptables
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 5000 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 5000 -j ACCEPT
sudo service iptables save
```

## 🧪 Тестирование

### 1. Проверка сервисов
```bash
# Проверка статуса сервисов
sudo systemctl status tg-psy-webhook
sudo systemctl status tg-psy-bot

# Проверка логов
sudo journalctl -u tg-psy-webhook -f
sudo journalctl -u tg-psy-bot -f
```

### 2. Проверка webhook
```bash
# Проверка health check
curl http://YOUR_DOMAIN.com/health

# Тест webhook
curl -X POST http://YOUR_DOMAIN.com/sales/prodamus \
  -H "Content-Type: application/json" \
  -H "Sign: test_signature" \
  -d '{"test": "data"}'
```

### 3. Проверка конфигурации
```bash
# Проверка конфигурации
cd /opt/tg_psy
source venv/bin/activate
python3 check_config.py
```

## 📝 Настройка в панели Prodamus

### 1. Webhook URL
- **URL**: `https://YOUR_DOMAIN.com/sales/prodamus`
- **Метод**: POST
- **Заголовки**: `Sign: {signature}`

### 2. Настройки магазина
- **Shop ID**: `dashastar`
- **Secret Key**: `b2f9e8a399225271521dfe88a277a7371cb8c2cebfeaa6f0276ba81fcc303c93`
- **Demo Mode**: Включен для тестирования

## 🔍 Мониторинг и логи

### 1. Логи приложения
```bash
# Логи webhook
sudo journalctl -u tg-psy-webhook -f

# Логи бота
sudo journalctl -u tg-psy-bot -f

# Логи Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### 2. Мониторинг ресурсов
```bash
# Проверка использования ресурсов
htop
df -h
free -h

# Проверка портов
netstat -tlnp | grep :5000
```

## ⚠️ Важные замечания

### 1. Безопасность
- ✅ Используйте HTTPS для продакшена
- ✅ Настройте файрвол
- ✅ Регулярно обновляйте систему
- ✅ Используйте сильные пароли

### 2. Резервное копирование
- ✅ Регулярно создавайте резервные копии базы данных
- ✅ Сохраняйте конфигурационные файлы
- ✅ Документируйте изменения

### 3. Производительность
- ✅ Мониторьте использование ресурсов
- ✅ Настройте логирование
- ✅ Используйте мониторинг системы

## 🚨 Устранение неполадок

### Проблема: Сервисы не запускаются
**Решение:**
```bash
# Проверка логов
sudo journalctl -u tg-psy-webhook -n 50
sudo journalctl -u tg-psy-bot -n 50

# Перезапуск сервисов
sudo systemctl restart tg-psy-webhook
sudo systemctl restart tg-psy-bot
```

### Проблема: Webhook не получает уведомления
**Решение:**
```bash
# Проверка доступности
curl -I https://YOUR_DOMAIN.com/sales/prodamus

# Проверка Nginx
sudo nginx -t
sudo systemctl reload nginx
```

### Проблема: SSL сертификат не работает
**Решение:**
```bash
# Обновление сертификата
sudo certbot renew --dry-run

# Проверка конфигурации Nginx
sudo nginx -t
```

---

**Система готова к развертыванию на Linux сервере! 🚀**
